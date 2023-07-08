/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["core/templates/*.html",
            "client/templates/clients/*.html",
            "leads/templates/leads/*.html",
            "user_profile/templates/user_profile/*.html",
            "team/templates/team/*.html",
            "dashboard/templates/dashboard/*.html",
            "static/js/*.js"  

],
  theme: {
    extend: {},
  },
  plugins: [],
}

