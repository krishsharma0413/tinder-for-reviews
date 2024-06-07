/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/*.html"],
  theme: {
    extend: {
      colors:{
        "primary": "#ffffff",
        "background": "#161618",
        "accentgreen": "#2ddd6a",
        "accentred": "#d51f68"
      },
      fontFamily: {
        "sharetechmono": ["Share Tech Mono", "monospace"],
      },
    },
  },
  plugins: [],
}

