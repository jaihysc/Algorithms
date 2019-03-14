/* eslint-disable no-undef */
/* eslint-disable no-console */
//Uses tensorflow.js
let xPoints = []; //Stores points
let yPoints = [];

//Slope and Y-int for line
let m, b;

const learningRate = 0.5;
const optimizer = tf.train.sgd(learningRate);

// eslint-disable-next-line no-unused-vars
function setup() {
	createCanvas(600, 600);

	//Add some default values to the x and y points
	// xPoints.push(0.1);
	// xPoints.push(0);
	// yPoints.push(0.2);
	// yPoints.push(0.15);

	//Because these are variables, tf defaults to adjust these when optimizing
	//Since I am not passing it a var list
	m = tf.variable(tf.scalar(random(1))); //Randomly get a number for slope
	b = tf.variable(tf.scalar(random(1))); //tf.variable to allow the value to change
}

//Main
/**
 * Normalizes val to number between 0 - 1
 * @param {Number} val 
 * @param {Number} max 
 * @param {Number} min 
 */
function normalize(val, max, min) { 
	return (val - min) / (max - min); 
}
/**
 * Denormalizes a number between 0 - 1 to between min and max
 * @param {number} val 
 * @param {number} max 
 * @param {number} min 
 */
function deNormalize(val, max, min) {
	return (val - min) * max;
}

function predict(xArr) {
	//convert x array into tensor
	const xTens = tf.tensor1d(xArr);

	//y = mx + b
	const yTens = xTens.mul(m).add(b); //Apply line formula to x
	return yTens;
}
function loss(pred, labels) {
	return pred.sub(labels).square().mean();
}

// eslint-disable-next-line no-unused-vars
function mousePressed() {
	//Normalize points to 0 - 1
	const norXPoint = normalize(mouseX, width, 0); // Value, originalStart, orignalEnd, newStart, newEnd
	const norYPoint = normalize(mouseY, height, 0);

	//Add to list
	xPoints.push(norXPoint);
	yPoints.push(norYPoint);

	//console.log(xPoints, yPoints);
}

// eslint-disable-next-line no-unused-vars
function draw() {
	//Only optimize if we have some variables
	if (xPoints.length > 1) {
		tf.tidy(() => {
			const yTens = tf.tensor1d(yPoints);
			optimizer.minimize(() => loss(predict(xPoints), yTens)); //Optimize with predict and loss
		});
	}
	
	background(0, 0, 0);
	stroke(255);
	strokeWeight(8);
	
	//Denormalizes and draws the points
	for (let i = 0; i < xPoints.length; i++) {
		let px = deNormalize(xPoints[i], width, 0);
		let py = deNormalize(yPoints[i], height, 0);

		point(px, py);		
	}

	//Don't forget to clean up!!
	//Take 2 points and draw it
	const xs = [0, 1]; // bottom and top
	const ys = tf.tidy(() => predict(xs));

	//Denormalize
	let x1 = map(xs[0], 0, 1, 0, width);
	let x2 = map(xs[1], 0, 1, 0, width);

	//Get the values of ys back from tensors
	let lineY = ys.dataSync();
	let y1 = map(lineY[0], 0, 1, 0, height); // switch 0, height around to make it perpendicular
	let y2 = map(lineY[1], 0, 1, 0, height);

	strokeWeight(1);
	stroke(255, 0, 0);
	line(x1, y1, x2, y2);
	stroke(0);
	
	ys.dispose();
	
	fill(255);
	text("0, 0 at top left", 10, height - 30);
	text("y = " + (m.dataSync() * -1) + "x + " + (b.dataSync() * -1), 10, height - 10);
	//Multiply everything by -1 to invert it since X Y counts from top left
	//console.log(tf.memory().numTensors);
	//noLoop();
}