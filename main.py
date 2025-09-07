#!/usr/bin/env python3
"""
dkim-splitter: A CLI tool to split long DKIM TXT records
into 255-character chunks for AWS Route 53 (or any DNS provider).

"""

import argparse
import sys
import textwrap


# --- Utility Functions --- #
def split_txt_record(value: str, chunk_size: int = 255) -> list[str]:
    """Split a TXT record into chunks of <= 255 characters."""
    value = value.strip().strip('"')  # remove accidental quotes
    return [value[i : i + chunk_size] for i in range(0, len(value), chunk_size)]


def format_chunks(chunks: list[str]) -> str:
    """Format chunks into Route 53–ready TXT record."""
    return " ".join(f"\"{chunk}\"" for chunk in chunks)


def print_banner():
    banner = r"""
    
      :::::::::  :::    ::: :::::::::::   :::   :::                  ::::::::  :::::::::  :::        ::::::::::: ::::::::::: ::::::::::: :::::::::: ::::::::: 
     :+:    :+: :+:   :+:      :+:      :+:+: :+:+:                :+:    :+: :+:    :+: :+:            :+:         :+:         :+:     :+:        :+:    :+: 
    +:+    +:+ +:+  +:+       +:+     +:+ +:+:+ +:+               +:+        +:+    +:+ +:+            +:+         +:+         +:+     +:+        +:+    +:+  
   +#+    +:+ +#++:++        +#+     +#+  +:+  +#+ +#++:++#++:++ +#++:++#++ +#++:++#+  +#+            +#+         +#+         +#+     +#++:++#   +#++:++#:    
  +#+    +#+ +#+  +#+       +#+     +#+       +#+                      +#+ +#+        +#+            +#+         +#+         +#+     +#+        +#+    +#+    
 #+#    #+# #+#   #+#      #+#     #+#       #+#               #+#    #+# #+#        #+#            #+#         #+#         #+#     #+#        #+#    #+#     
#########  ###    ### ########### ###       ###                ########  ###        ########## ###########     ###         ###     ########## ###    ###      


    DKIM Splitter - Make long DKIM keys Route 53 friendly
    """
    print(banner)


# --- Main CLI --- #
def main():
    parser = argparse.ArgumentParser(
        description="Split long DKIM TXT records into 255-char chunks for Route 53"
    )
    parser.add_argument(
        "dkim",
        nargs="?",
        help="DKIM key string (if not provided, will read from stdin or file)",
    )
    parser.add_argument(
        "-f", "--file", help="Read DKIM key from a file instead of argument/stdin"
    )
    parser.add_argument(
        "-o", "--output", help="Write the split result to a file instead of stdout"
    )
    parser.add_argument(
        "-q", "--quiet", action="store_true", help="Suppress banner and extra info"
    )
    args = parser.parse_args()

    if not args.quiet:
        print_banner()

    # Load DKIM key
    if args.file:
        try:
            with open(args.file, "r", encoding="utf-8") as f:
                dkim_value = f.read().strip()
        except Exception as e:
            sys.exit(f"❌ Error reading file: {e}")
    elif args.dkim:
        dkim_value = args.dkim.strip()
    else:
        if not args.quiet:
            print("🔑 Paste your DKIM key (single line), then press Enter:")
        dkim_value = sys.stdin.readline().strip()

    if not dkim_value:
        sys.exit("❌ No DKIM key provided.")

    # Split into chunks
    chunks = split_txt_record(dkim_value)

    # Validation
    too_long = [c for c in chunks if len(c) > 255]
    if too_long:
        sys.exit("❌ Error: One or more chunks exceed 255 characters.")

    # Format for Route 53
    formatted = format_chunks(chunks)

    # Output
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(formatted + "\n")
        if not args.quiet:
            print(f"✅ DKIM record written to {args.output}")
    else:
        if not args.quiet:
            print("\n✅ Route 53–ready DKIM record:\n")
        print(formatted)
        if not args.quiet:
            print(
                textwrap.dedent(
                    f"""
                    📋 Copy & paste this into Route 53 TXT record value field.
                    ℹ️  Total length: {len(dkim_value)} chars
                    ℹ️  Split into {len(chunks)} chunks (max {max(len(c) for c in chunks)} chars each)
                    """
                )
            )


if __name__ == "__main__":
    main()