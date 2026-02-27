"""
Shanks CLI - Backward compatibility wrapper

This file maintains backward compatibility with the old cli.py structure.
The actual implementation has been modularized into shanks/cli/ package.
"""

from shanks.cli.main import main
from shanks.cli.sorm import sorm_main

# Re-export for backward compatibility
__all__ = ["main", "sorm_main"]

if __name__ == "__main__":
    main()
