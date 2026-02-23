# How to Publish VSCode Extension

## Prerequisites

1. Install vsce (Visual Studio Code Extension Manager):
```bash
npm install -g @vscode/vsce
```

2. Create a publisher account:
   - Go to https://marketplace.visualstudio.com/manage
   - Sign in with Microsoft account
   - Create a publisher

## Build Extension

1. Navigate to extension directory:
```bash
cd vscode-extension
```

2. Package the extension:
```bash
vsce package
```

This creates a `.vsix` file (e.g., `shanks-django-0.1.0.vsix`)

## Publish to Marketplace

1. Get Personal Access Token (PAT):
   - Go to https://dev.azure.com
   - User Settings → Personal Access Tokens
   - Create new token with "Marketplace (Manage)" scope

2. Login to vsce:
```bash
vsce login <publisher-name>
```

3. Publish:
```bash
vsce publish
```

Or publish specific version:
```bash
vsce publish minor  # 0.1.0 -> 0.2.0
vsce publish major  # 0.1.0 -> 1.0.0
vsce publish patch  # 0.1.0 -> 0.1.1
```

## Manual Installation (for testing)

1. Package the extension:
```bash
vsce package
```

2. Install in VSCode:
   - Open VSCode
   - Go to Extensions (Ctrl+Shift+X)
   - Click "..." menu
   - Select "Install from VSIX..."
   - Choose the `.vsix` file

## Update Extension

1. Update version in `package.json`
2. Update `CHANGELOG.md`
3. Package and publish:
```bash
vsce package
vsce publish
```

## Unpublish Extension

```bash
vsce unpublish <publisher>.<extension-name>
```

## Resources

- [VSCode Extension Publishing](https://code.visualstudio.com/api/working-with-extensions/publishing-extension)
- [Marketplace](https://marketplace.visualstudio.com/)
