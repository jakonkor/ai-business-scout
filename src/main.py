"""
AI Business Scout - Main Application
Orchestrates the multi-agent pipeline for business idea generation and validation
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from src.agents import (
    WebScannerAgent,
    IdeaGeneratorAgent,
    BusinessAnalystAgent,
    MarketValidatorAgent,
)
from src.models import ScoutReport
from src.utils.config import config, Config

console = Console()


class BusinessScout:
    """Main orchestrator for the business scouting pipeline"""
    
    def __init__(self):
        self.scanner = WebScannerAgent()
        self.generator = IdeaGeneratorAgent()
        self.analyst = BusinessAnalystAgent()
        self.validator = MarketValidatorAgent()
    
    async def run_full_pipeline(
        self,
        max_ideas: int = 5,
        validation_budget_per_idea: float = 500.0,
        validation_duration_days: int = 7,
        save_report: bool = True
    ) -> ScoutReport:
        """
        Run the complete business scouting pipeline.
        
        Args:
            max_ideas: Maximum number of ideas to generate
            validation_budget_per_idea: Budget per validation campaign
            validation_duration_days: Duration for validation campaigns
            save_report: Whether to save report to file
        
        Returns:
            Complete scout report
        """
        console.print(Panel.fit(
            "🚀 [bold cyan]AI Business Scout[/bold cyan]\n"
            "Discovering and Validating Business Opportunities",
            border_style="cyan"
        ))
        
        # Phase 1: Web Scanning
        console.print("\n[bold]Phase 1: Web Scanning[/bold]", style="yellow")
        trends = await self.scanner.scan_all_sources()
        
        if not trends:
            console.print("❌ No trends found. Please configure API keys in .env", style="red")
            return None
        
        # Phase 2: Idea Generation
        console.print("\n[bold]Phase 2: Idea Generation[/bold]", style="yellow")
        ideas = await self.generator.generate_ideas(trends, max_ideas=max_ideas)
        
        # Phase 3: Business Analysis
        console.print("\n[bold]Phase 3: Business Analysis[/bold]", style="yellow")
        analyses = await self.analyst.analyze_ideas(ideas)
        
        # Phase 4: Market Validation
        console.print("\n[bold]Phase 4: Market Validation[/bold]", style="yellow")
        validations = await self.validator.validate_ideas(
            ideas=ideas,
            analyses=analyses,
            budget_per_idea=validation_budget_per_idea,
            duration_days=validation_duration_days
        )
        
        # Generate Report
        report = self._generate_report(trends, ideas, analyses, validations)
        
        # Display Summary
        self._display_summary(report)
        
        # Save Report
        if save_report:
            self._save_report(report)
        
        return report
    
    def _generate_report(self, trends, ideas, analyses, validations) -> ScoutReport:
        """Generate comprehensive report"""
        
        # Generate top recommendations
        top_recommendations = []
        
        promising_validations = [v for v in validations if v.is_promising]
        
        if promising_validations:
            top_recommendations.append(
                f"🎯 {len(promising_validations)} out of {len(validations)} ideas show strong market validation"
            )
            
            for validation in promising_validations:
                idea = next(i for i in ideas if i.id == validation.idea_id)
                analysis = next(a for a in analyses if a.idea_id == idea.id)
                
                top_recommendations.append(
                    f"✨ '{idea.title}' - Viability: {analysis.viability_score:.1f}/10, "
                    f"Engagement: {validation.metrics.engagement_score:.1f}/10"
                )
        else:
            top_recommendations.append(
                "⚠️ No ideas achieved strong validation - consider refining approach"
            )
        
        return ScoutReport(
            trends_found=trends,
            ideas_generated=ideas,
            analyses=analyses,
            validations=validations,
            top_recommendations=top_recommendations
        )
    
    def _display_summary(self, report: ScoutReport):
        """Display summary in terminal"""
        
        console.print("\n" + "="*70)
        console.print("[bold green]📊 EXECUTIVE SUMMARY[/bold green]")
        console.print("="*70 + "\n")
        
        # Stats table
        stats_table = Table(show_header=True, header_style="bold magenta")
        stats_table.add_column("Metric", style="cyan")
        stats_table.add_column("Value", justify="right", style="green")
        
        stats_table.add_row("Trends Analyzed", str(len(report.trends_found)))
        stats_table.add_row("Ideas Generated", str(len(report.ideas_generated)))
        stats_table.add_row("Ideas Validated", str(len(report.validations)))
        
        promising = len([v for v in report.validations if v.is_promising])
        stats_table.add_row("Promising Ideas", str(promising))
        
        console.print(stats_table)
        
        # Top Recommendations
        console.print("\n[bold]🎯 Top Recommendations:[/bold]")
        for rec in report.top_recommendations:
            console.print(f"  {rec}")
        
        # Top Ideas Details
        if report.validations:
            console.print("\n[bold]💡 Top Ideas (by validation):[/bold]\n")
            
            sorted_validations = sorted(
                report.validations,
                key=lambda v: v.metrics.engagement_score,
                reverse=True
            )
            
            for i, validation in enumerate(sorted_validations[:3], 1):
                idea = next(i for i in report.ideas_generated if i.id == validation.idea_id)
                analysis = next(a for a in report.analyses if a.idea_id == idea.id)
                
                status = "✅" if validation.is_promising else "⚠️"
                
                console.print(f"{status} [bold]{i}. {idea.title}[/bold]")
                console.print(f"   Viability Score: {analysis.viability_score:.1f}/10")
                console.print(f"   Engagement Score: {validation.metrics.engagement_score:.1f}/10")
                console.print(f"   CTR: {validation.metrics.ctr*100:.2f}% | "
                            f"Conversions: {validation.metrics.conversions} | "
                            f"CPC: ${validation.metrics.cpc:.2f}")
                console.print(f"   {idea.value_proposition}\n")
        
        console.print("="*70 + "\n")
    
    def _save_report(self, report: ScoutReport):
        """Save report to file"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"scout_report_{timestamp}.json"
        filepath = config.DATA_DIR / filename
        
        # Convert report to dict for JSON serialization
        report_dict = {
            "generated_at": report.generated_at.isoformat(),
            "trends_found": [t.model_dump() for t in report.trends_found],
            "ideas_generated": [i.model_dump() for i in report.ideas_generated],
            "analyses": [a.model_dump() for a in report.analyses],
            "validations": [v.model_dump() for v in report.validations],
            "top_recommendations": report.top_recommendations
        }
        
        with open(filepath, 'w') as f:
            json.dump(report_dict, f, indent=2, default=str)
        
        console.print(f"\n💾 Report saved to: [cyan]{filepath}[/cyan]")


async def main():
    """Main entry point"""
    
    # Validate configuration
    if not Config.validate():
        console.print("\n❌ Configuration incomplete. Please check your .env file.", style="red")
        console.print("Copy .env.example to .env and add your API keys.", style="yellow")
        return
    
    # Run pipeline
    scout = BusinessScout()
    await scout.run_full_pipeline(
        max_ideas=5,
        validation_budget_per_idea=500.0,
        validation_duration_days=7
    )


if __name__ == "__main__":
    asyncio.run(main())
