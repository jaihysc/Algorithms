/* eslint-disable no-undef */
/* eslint-disable no-console */
//Uses tensorflow.js
let xPoints = []; //Stores points
let yPoints = [];

//Slope and Y-int for line
let a, b, c;

const learningRate = 0.3;
const optimizer = tf.train.adam(learningRate); //Different algorithems may be faster for certain applications

// eslint-disable-next-line no-unused-vars
function setup() {
	createCanvas(600, 600);

	//Because these are variables, tf defaults to adjust these when optimizing
	//Since I am not passing it a var list
	a = tf.variable(tf.scalar(random(1))); //Randomly get a number for slope
	b = tf.variable(tf.scalar(random(1))); //tf.variable to allow the value to change
	c = tf.variable(tf.scalar(random(1)));
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
	const xTsrs = tf.tensor1d(xArr);

	//y = ax^2 + bx + c
	const yTsrs = xTsrs.square().mul(a).add(xTsrs.mul(b)).add(c);
	return yTsrs;
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
	
	//Draw the curve
	const curveX = []; //Store points for the curve
	for (let i = 0; i <= 1; i += 0.005) {
		curveX.push(i);
	}
	//console.log(curveX);

	const ys = tf.tidy(() => predict(curveX));

	//Get the values of ys back from tensors
	let curveY = ys.dataSync();

	//Draw the parabola
	beginShape();
	strokeWeight(1);
	stroke(255, 0, 0);
	noFill();
	for (let i = 0; i < curveX.length; i++) {
		let x = map(curveX[i], 0, 1, 0, width);
		let y = map(curveY[i], 0, 1, 0, height);

		vertex(x, y);
	}
	endShape();
	stroke(0);

	//Print the formula
	fill(255);
	//y = ax^2 + bx + c
	text("0, 0 at top left", 10, height - 30)
	text("y = " + (a.dataSync() * -1) + "x^2 + " + (b.dataSync() * -1) + "x + " + (c.dataSync() * -1), 10, height - 10);
	//Multiply everything by -1 to invert as 0,0 is at top left
	
	ys.dispose();

	//console.log(tf.memory().numTensors);
	//noLoop();
}