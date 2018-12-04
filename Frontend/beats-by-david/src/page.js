import React from "react"
import map from "./mapEC.png"
import './style.css'

class Page extends React.Component{
	render (){
		return (<body>
  <link href='//fonts.googleapis.com/css?family=Roboto+Condensed:300,400,700' rel='stylessheet' type='text/css' />
<link href='//fonts.googleapis.com/css?family=Roboto:100,300,400,700,900' rel='stylessheet' type='text/css' />

<h1>CU Boulder Engineering Center</h1>
<p class="description"> We're here to help you find a peaceful and productive place to study. Don't deal with loud and overly hot areas of the Engineering Center again. <strong>Click the points to expand them.</strong></p>
<div class="distribution-map" styles="width:50%; height: auto;">
    <img src= {map} alt="EC map"/>
    <button class="map-point" styles="top:26%;left:31.5%">
        <div class="content">
            <div class="centered-y">
                <h2>ECEA</h2>
                <p>Looks like its ___ degrees and medium volume. <a href="ecea.html" styles="text-transform: capitalize;"><br/></a></p>
            </div>
        </div>
    </button>
    <button class="map-point" styles="top:53%;left:41.5%">
        <div class="content">
            <div class="centered-y">
                <h2>Main Lobby</h2>
                <p>Looks like its ___ degrees and medium volume. <a href="ml.html" styles="text-transform: capitalize;"><br/>Click here for the daily trend.</a></p>
            </div>
        </div>
    </button>
    <button class="map-point" styles="top:66.5%;left:77%">
        <div class="content">
            <div class="centered-y">
                <h2>ITLL</h2>
                <p>Looks like its ___ degrees and medium volume. <a href="itll.html" styles="text-transform: capitalize;"><br/>Click here for the daily trend.</a></p>
            </div>
        </div>
    </button>
    <button class="map-point" styles="top:75%;left:25%">
        <div class="content">
            <div class="centered-y">
                <h2>South Lobby</h2>
                <p>Looks like its ___ degrees and medium volume. <a href="sl.html" styles="text-transform: capitalize;"><br/>Click here for the daily trend.</a></p>
            </div>
        </div>
    </button>
    <button class="map-point" styles="top:78.5%;left:17%">
        <div class="content">
            <div class="centered-y">
                <h2>CSEL</h2>
                <p>Looks like its ___ degrees and medium volume. <a href="csel.html" styles="text-transform: capitalize;"><br/>Click here for the daily trend.</a></p>
            </div>
        </div>
    </button>
    <button class="map-point" styles="top:34.5%;left:75%">
        <div class="content">
            <div class="centered-y">
                <h2>Discovery Learning Center</h2>
                <p>Looks like its ___ degrees and medium volume. <a href="dlc.html" styles="text-transform: capitalize;"><br/>Click here for the daily trend.</a></p>
            </div>
        </div>
    </button>
</div>
<a id="link" href="form.html" styles="text-transform: capitalize; hover-color: red;">About Us</a>
<styles>

</styles>
  <script src='http://ajax.googleapis.com/ajax/libs/angularjs/1.3.2/angular.min.js' />


</body> )
	}
}

export default Page;