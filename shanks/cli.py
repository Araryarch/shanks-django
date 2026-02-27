"""
Shanks CLI - Backward compatibility wrapper

This file maintains backward compatibility with the old cli.py structure.
The actual implementation has been modularized into shanks/cli/ package.
"""

from shanks.cli.main import main

# Re-export for backward compatibility
__all__ = ["main"]

if __name__ == "__main__":
    main()
