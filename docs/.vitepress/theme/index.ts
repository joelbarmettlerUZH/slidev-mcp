import DefaultTheme from "vitepress/theme";
import HomeLayout from "./HomeLayout.vue";
import ObfuscatedEmail from "./components/ObfuscatedEmail.vue";
import "./custom.css";

export default {
  extends: DefaultTheme,
  Layout: HomeLayout,
  enhanceApp({ app }) {
    app.component("ObfuscatedEmail", ObfuscatedEmail);
  },
};
