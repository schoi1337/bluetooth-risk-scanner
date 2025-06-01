import argparse
import asyncio
from main import run_scan
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

def print_banner():
    banner_text = """

┌┐ ┬  ┬ ┬┌─┐┌┬┐┌─┐┌─┐┌┬┐┬ ┬   ┬─┐┬┌─┐┬┌─   ┌─┐┌─┐┌─┐┌┐┌┌┐┌┌─┐┬─┐
├┴┐│  │ │├┤  │ │ ││ │ │ ├─┤───├┬┘│└─┐├┴┐───└─┐│  ├─┤││││││├┤ ├┬┘
└─┘┴─┘└─┘└─┘ ┴ └─┘└─┘ ┴ ┴ ┴   ┴└─┴└─┘┴ ┴   └─┘└─┘┴ ┴┘└┘┘└┘└─┘┴└─
Author: @schoi1337                                                                                                                   

    """
    console.print(Panel(Text(banner_text, justify="center", style="bold cyan"), expand=False))

def print_info(msg):
    console.print(f"[bold green][INFO][/bold green] {msg}")

def print_warning(msg):
    console.print(f"[bold yellow][WARNING][/bold yellow] {msg}")

def print_error(msg):
    console.print(f"[bold red][ERROR][/bold red] {msg}")

def print_success(msg):
    console.print(f"[bold blue][SUCCESS][/bold blue] {msg}")

def parse_args():
    parser = argparse.ArgumentParser(description="Bluetooth Risk Scanner CLI")
    parser.add_argument("--timeout", type=int, default=10, help="BLE scan timeout in seconds")
    parser.add_argument("--interval", type=int, default=0, help="Batch scan interval in minutes (0 = run once)")
    parser.add_argument("--json-only", action="store_true", help="Output JSON report only")
    parser.add_argument("--html-only", action="store_true", help="Output HTML report only")
    parser.add_argument("--offline", type=str, help="Analyze stored JSON file instead of scanning")
    return parser.parse_args()

async def batch_scan(args):
    print_banner()
    while True:
        print_info(f"Starting BLE scan with timeout={args.timeout}s")
        devices = await run_scan(
            timeout=args.timeout,
            json_only=args.json_only,
            html_only=args.html_only,
            offline=args.offline
        )
        print_success("Scan completed successfully.")
        print_info(f"Total devices scanned: {len(devices)}")
        for dev in devices:
            print(f"- {dev.get('name', 'Unknown')} ({dev.get('vendor_name', 'Unknown')}), Risk: {dev.get('risk_level', 'N/A')}")
            if dev.get("cve_summary"):
                print("  CVEs:")
                for cve in dev["cve_summary"]:
                    print(f"    {cve['id']} [{cve['cvss']}]: {cve['desc'][:60]}...")
        if args.interval <= 0:
            break
        print_info(f"Waiting {args.interval} minutes until next scan...")
        await asyncio.sleep(args.interval * 60)

def main():
    args = parse_args()
    asyncio.run(batch_scan(args))

if __name__ == "__main__":
    main()
