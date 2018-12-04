import React from "react"
import map from "./mapEC.png"
import './style.css'
import { Button, Popovers} from 'react-bootstrap'
import { Chart } from "react-google-charts";

class Page extends React.Component{
	render (){
		return (<body>

<h1>CU Boulder Engineering Center</h1>
<p class="description"> We're here to help you find a peaceful and productive place to study. Don't deal with loud and overly hot areas of the Engineering Center again. <strong>Click the points to expand them.</strong></p>
<div class="distribution-map" styles="width:50%; height: auto;">
    <img src= {map} alt="EC map"/>
    <button class="btn1"></button>
    <button class="btn2"></button>
    <button class="btn3"></button>
    <button class="btn5"></button>
    <button class="btn6"></button>
</div>
<a id="link" href="form.html" styles="text-transform: capitalize; hover-color: red;">About Us</a>
<styles>

</styles>
  <script src='http://ajax.googleapis.com/ajax/libs/angularjs/1.3.2/angular.min.js' />

</body>)
	}
}

export default Page;
