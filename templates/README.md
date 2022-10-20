# What is this?

I was having an annoying issue. Which is, I had to install packages and setup environments every time I make a new tailwindcss project. So I thought making an template will help a lot and this repo is just the thing.

&nbsp;
&nbsp;

# Features

- Basic TailWindCSS Setup
- Autoprefixier Setup
- Prettier for TailwindCSS
- Necessary VSCode settings for the workspace
- Necessary build scripts

&nbsp;
&nbsp;

# Pre-Requirements

- Node.js
- VSCode Editor
- Prettier Plugin in VSCode

&nbsp;
&nbsp;

# How to use?

### Just follow these steps:

- Clone the repo
  `git clone https://github.com/Ahsan40/tw-css-template.git`
- Open the dir `cd tw-css-template`
- Install npm packages
  `npm install`
- Remove `README.md` file and `.git` folder
- Configure `package.json` and `tailwind.config.js` to your needs

and we are done. Happy coding...

&nbsp;
&nbsp;

# Commands

### Command format

```bash
npm run cmd
```

&nbsp;

### Available CMD

- `build:styles` : build styles.css from src dir using jit compiler and keep watching for changes in public folder.
- `build:production` : build styles.css from src but the size will be a lot smaller which is also called min version or minify.

&nbsp;

### Examples

```bash
npm run build:styles
```

```bash
npm run build:production
```

Note: These commands should works on all os.

&nbsp;
&nbsp;

# Info

Well, I am using windows so I've made some scripts which will make life a little easier for windows users.

- `watch-all` : This file will build the styles with tailwind `jit` compiler and keep watching. Whenever there is change in any file inside `public` folder, css will be build again.
- `build-all` : This file will do the same thing like the previous one the only exception is that the generated file with this script will be a lot smaller. As the file name stated, you should use it when the design is done and project is ready to launch. Also this script won't keep watching for the changes as this is the final product

&nbsp;
&nbsp;

# Want to help?

Well, if you are interested in helping/improving this template feel free to do so. It will help me and other people (if anyone use it at all) a lot.
