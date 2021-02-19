module.exports = {
    "extends": "airbnb-base",
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
    "rules": {}
};
