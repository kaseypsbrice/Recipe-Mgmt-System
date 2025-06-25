# irms-app

This template should help get you started developing with Vue 3 in Vite.

## Recommended IDE Setup

[VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur).

## Customize configuration

See [Vite Configuration Reference](https://vite.dev/config/).

## Project Setup

```sh
npm install
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Compile and Minify for Production

```sh
npm run build
```

### Run Unit Tests with [Vitest](https://vitest.dev/)

```sh
npm run test:unit
```

## Workplace Settings in VScode

It took me a while to figure this out.

The extension for Tailwind CSS Intellisense might not work in vscode when working with Vue.js.
Intellisense is responsible for auto-complete suggestions, so it's preferable to have it enabled.

To resolve this issue:

* CTRL+SHIFT+P
* Type "Open Workspace Settings (JSON)" and select the corresponding suggestion
* Copy the below configuration
* Add it to settings.json
* Restart VScode

```
{
"tailwindCSS.experimental.configFile": "src/assets/index.css",
  "editor.quickSuggestions": {
    "strings": true
  }
}
```