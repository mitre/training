module.exports = {
    "extends": "eslint:recommended",
    "env": {
        "browser": true,
        "es2021": true,
        "jquery": true,
    },
    "parserOptions": {
        "ecmaVersion": 12
    },
    "globals": {
        stream: "readonly",
        restRequest: "readonly",
        certificates: "readonly",
    },
    "rules": {
        semi: ["error", "always"],
        quotes: ["error", "single", {"avoidEscape": true }]
    }
};
