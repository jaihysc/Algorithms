module.exports = {
	"env": {
		"browser": true,
		"es6": true,
		"node": true
	},
	"globals": {
		"Atomics": "readonly",
		"SharedArrayBuffer": "readonly"
	},
	"parserOptions": {
		"ecmaVersion": 2018,
		"sourceType": "module"
	},
	"rules": {
		"indent": [
			"error",
			"tab"
		],
		"linebreak-style": [
			"error",
			"unix"
		],
		"quotes": [
			"error",
			"double"
		],
		"semi": [
			"error",
			"always"
		]
	},
	"extends": [
		"eslint:recommended",
        "p5js",
        "p5js/dom",
        "p5js/sound"
    ]
};