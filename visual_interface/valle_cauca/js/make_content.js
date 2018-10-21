var fullsito = {
    'Name': "Welcome to geolocarti.",
    'lat': 3.435911,'lng': -76.564844,
    'Content': 'Por favor sea cuidadoso y anotar las observacions. Gracias!',
    'Radio': 13200, 'Zoom': 18, 'count': 'loaded',
    'country':'Colombia',
    'city':'Cali',
    'region':'Valle del Cauca',
    'logo_path':'../../../downloads/presentation.png',
    'affid':60066812
  };

function makeContent(full_obj=fullsito){

  var cont = `
      <div class="col-title">
        <p>${full_obj.Name}</p>
      </div>

  <div class="container-fluid" id="col-container">

    <div class="mainbody" id="scrollable_body">

      <div class="row">
          <div class="column" >
            <img src="${full_obj.logo_path}" id="logo_image" style="width:100%;max-width:150px;">
          </div>
          <div class="column" >
            <ul style="list-style-type:none">
              <li>Country: ${full_obj.country}</li>
              <li>Region: ${full_obj.region}</li>
              <li>City: ${full_obj.city}</li>
              <li>Repetitions: ${full_obj.count}</li>
              <li>Scopus ID: <label id="scopus_id_tofind">${full_obj.affid}</label></li>
            </ul>
          </div>
      </div>

      <div id="z" class="body" style="width:100%">
        <p style="font-size:11px;">Investigación en desarrollo, <a href="http://www.univalle.edu.co">Universidad del Valle</a>.
        </p>
      </div>
      <div id="y" class="body">${full_obj.Content}
      </div>

      <div class="row" style="margin-top: 5px; border: solid 1px; border-radius: 8px; margin-right: 10px;">

        <div class="column" style="margin-left: 10px; width:49%;">
            <label> Region type:
            <select id="which_region">
              <option value="city">City</option>
              <option value="state">State</option>
              <option value="country">Country</option>
            </select>
            </label>
        </div>

        <div class="column" style="margin-left:-4px;">
        <label> Sub-Region:
            <select id="which_subRegion">
              <option value="city">City</option>
              <option value="state">State</option>
              <option value="country">Country</option>
            </select>
            </label>
        </div>

      </div>

      <div class="row" style="margin-top: 5px;">

        <div class="column" >

          <form>
            <input class="MyButton" type="button" value="Inside of region" label="sparqlQuery" id="button_inRegion"/>
          </form>
          <form>
            <input class="MyButton" type="button" value="Out of Region" id="button_offRegion"/>
          </form>
          <form>
            <input class="MyButton" type="button" value="In Region, Off Subreg" id="button_onRegion_offSubregion"/>
          </form>
          <form>
            <input class="MyButton" type="button" value="Off Region, In Subreg" id="button_offRegion_onSubregion"/>
          </form>
        </div>

        <div class="column" style="color:black; margin-left:4px;">

            <div style="border: solid 1px black; border-radius: 12px 8px 8px 12px;">
                <form>
                    <input class="MyButton" type="button" value="Country\'s network" id='button_drawAll'/>
                </form>
                <label> Country Code:
                    <input type="text" name="quantity" id="country_code" style="max-width:70px; border-radius: 0px 6px 6px 0px;">
                    </input>
                    <form>
                        <input class="MyButton" type="button" value="Node and country" id="node_country"/>
                    </form>
                </label>
            </div>

            <div style="border: solid 1px black; border-radius: 12px 8px 8px 12px;">
                <div style='padding-left:5px;'>
                    <label style="font-size:11px; font-weight:500; margin-right:-10px;">
                        Between regions?
                    <input class="plain_siwtch" type="checkbox" id="betweenRegions"  style="margin-left:-5px;">
                    </label>

                    <label> 2nd region:
                        <input type="text" name="quantity" id="second_region_name" style="max-width:70px; border-radius: 0px 6px 6px 0px;">
                        </input>
                    </label>
                </div>
            </div>

        </div>

      </div>
CIRCLES
      <div class="row" style="margin-top: 5px; border: solid 1px; border-radius: 8px; margin-right: 10px;">

        <div class="column_3" style="margin-left: 10px;">
             Circle 1:

                <input type="number" name="quantity" min="0.01" max="10100" step="0.5" value='50' id="circle1_radius" style="max-width:70px; border-radius: 6px 0px 0px 6px;">
                </input>


        </div>
        <div class="column_3" style="margin-left:4px;">
            <label> Circle 2:</label>
            <input type="number" name="quantity" min="0.01" max="10100" step="0.5" value='250' id="circle2_radius" style="max-width:70px; border-radius: 0px 6px 6px 0px;">
                </input>

        </div>

        <div class="column_extra" id="cluster_info" style="font-weight:bold; margin-left:4px; border-left-style: solid; border-left-color:green; border-left-width:2px; width:43%; float:left">
            There is still no clusterization made

        </div>

      </div>

      <div class="row" style="margin-top: 5px;">

        <div class="column" >
          <form>
            <input class="MyButton" type="button" value="Inside of circle 1" label="sparqlQuery" id="button_inCircle1"/>
          </form>
          <form>
            <input class="MyButton" type="button" value="Out of circle 1" id="button_offCircle1"/>
          </form>
          <form>
            <input class="MyButton" type="button" value="Off Circle 1, In Circle 2" id="button_offCircle1_onCircle2"/>
          </form>
          <form>
            <input class="MyButton" type="button" value="In Circle 1, Off Circle 2" id="button_onCircle1_offCircle2"/>
          </form>
        </div>

        <div class="column_3" style="color:white; margin-left:-15px; border-left-style: solid; border-left-color:blue; border-left-width:2px;">
          <form>
            <input class="MyButton" style="width: 75px;" type="button" value="Hide All" id='button_hideAll'/>
          </form>
          <form>
            <input class="MyButton" style="width: 75px;" type="button" value="Reset All" id='button_resetLinks'/>
          </form>
          <form>
            <input class="MyButton" style="width: 95px;" type="button" value="Active links" id='button_activeLinks'/>
          </form>
          <form>
            <input class="MyButton" style="width: 95px;" type="button" value="Active nodes" id='button_activeNodes'/>
          </form>
        </div>

        <div class="column_3" style="color:white; margin-left:0px; border-left-style: solid; border-left-color:green; border-left-width:2px;">
          <form>
            <input class="MyButton" style="width: 75px;" type="button" value="Table" id='button_statistics'/>
          </form>
          <form>
            <input class="MyButton" style="width: 75px;" type="button" value="clust Table" id='button_clusterStatistics'/>
          </form>
          <form>
            <input class="MyButton" style="width: 115px;" type="button" value="Clust. heatmap" id='button_clusterheatmap'/>
          </form>
          <form>
            <input class="MyButton" style="width: 105px;" type="button" value="Cluster nodes" id='button_clusterNodes'/>
          </form>
        </div>

      </div>

      <div id="innerbody" class="innside body">

      <h2 id="table_tittle"> Resultados </h2>
      <table>
  <tr>
    <th>Relación</th>
<th>Q affil</th>
<th>Weighted</th>
<th>Ave.</th>
    <th>\% affil</th>
    <th>\% weight</th>
  </tr>
  <tr>
    <td>Intra local</td>
    <td id="locality_absolute">-</td>
    <td id="locality_weighted">-</td>
    <td id="locality_average">-</td>
    <td id="locality_absolutePercentage">-</td>
    <td id="locality_weightedPercentage">-</td>
  </tr>
  <tr>
    <td>Inter local</td>
    <td id="region_absolute">-</td>
    <td id="region_weighted">-</td>
    <td id="region_average">-</td>
    <td id="region_absolutePercentage">-</td>
    <td id="region_weightedPercentage">-</td>
  <tr>
    <td>Supra local</td>
    <td id="supra_absolute">-</td>
    <td id="supra_weighted">-</td>
    <td id="supra_average">-</td>
    <td id="supra_absolutePercentage">-</td>
    <td id="supra_weightedPercentage">-</td>
  </tr>
  <tr>
    <td>Extra local</td>
    <td id="extra_absolute">-</td>
    <td id="extra_weighted">-</td>
    <td id="extra_average">-</td>
    <td id="extra_absolutePercentage">-</td>
    <td id="extra_weightedPercentage">-</td>
  </tr>
  <tr class="bordered">
    <td></td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>

  </tr>
  <tr>

    <td>TOTAL</td>
    <td id="total_absolute">-</td>
    <td id="total_weighted">-</td>
    <td id="total_average">-</td>
    <td id="total_absolutePercentage">&nbsp</td>
    <td id="total_weightedPercentage"></td>
  </tr>

</table>


        <p><b>Note:</b> The element will not take up any space when the display property set to "none".</p>
      </div>

      <div class="inner-footer">

        Footer
      </div>
  </div>

  `

  return cont

  };


 function infobox(){

   var checkbox = document.getElementById('info_chbx');

   if(checkbox.checked) {

       $("#info").show(1000);
   }

   else {
        $("#info").hide(1000);
    }

    };
/*document.getElementById("radius_size").onchange = function () {set_radius_multiplier()};*/

function set_radius_multiplier(){
    var multiplier = document.getElementById('radius_size').value;
    console.log(multiplier);
    console.log(radius_multiplier);
    radius_multiplier = multiplier;
};

