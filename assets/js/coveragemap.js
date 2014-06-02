(function($, exports) {
  if (typeof exports.Dexter == 'undefined') exports.Dexter = {};
  var Dexter = exports.Dexter;

  // view when looking at media coverage
  Dexter.CoverageView = function() {
    var self = this;

    // set global variables
    var form = $(".coverage-refine")
    var input_selected_province = form.find("input#selected_province")
    var input_selected_municipality = form.find("input#selected_municipality")
    var span_title = $("#map-area-title")

    var selected_province = input_selected_province.val()
    var selected_municipality = input_selected_municipality.val()

    if(selected_province)
      console.log(selected_province)
    else
      console.log("no province selected")
    if(selected_municipality)
      console.log(selected_municipality)
    else
      console.log("no municipality selected")

    // highlight selected province, fit map to province bounds, and load municipality shapes
    self.select_province = function(){

    }

    self.init = function() {
      // invalidate the map so that it gets resized correctly
      $($(this).attr('href') + ' .leaflet-container').each(function(i, map) {
        Dexter.maps.invalidate();
      });
      Dexter.maps.map.options.maxZoom = 8;

      self.load_title()

      Dexter.maps.drawProvinces(self.click_province);
      if(selected_province)
      {
        Dexter.maps.drawMunicipalities(selected_province, self.click_municipality);
      }

      self.load_and_draw_chart()
    };

    self.load_title = function(){
      if(selected_province)
      {
        var selected_level = "province"
        var selected_area_id = selected_province
        if(selected_municipality)
        {
          selected_level = "municipality"
          selected_area_id = selected_municipality
        }
        var query_str =  selected_level + '?filter[' + selected_level + ']=' + selected_area_id
        // load selected area's details from MAPS API
        $.getJSON("https://maps.code4sa.org/political/2011/" + query_str + '&quantization=5000', function (topo) {
          if (!topo)
            return;
          // set the page title
          console.log(topo.objects.demarcation.geometries[0])
          if(selected_level == "municipality")
            span_title.text(topo.objects.demarcation.geometries[0].properties.municipality_name)
          else
            span_title.text(topo.objects.demarcation.geometries[0].properties.province_name)
        });
      }
    }

    self.load_and_draw_chart = function(){
      // load chart data
      $.getJSON(Dexter.maps.placesUrl(), function(data){
        console.log(data)
        if(selected_province)
          data = data['provinces'][selected_province]
        if(selected_municipality)
          data = data['municipalities'][selected_municipality]
        if(data)
          self.drawChart(data);
        else
          $(".chart.chart-media-coverage").text("No data available.")
      });
    }

    self.click_province = function(province_id){
      input_selected_province.val(province_id);
      input_selected_municipality.val(null);
      selected_province = input_selected_province.val()
      selected_municipality = input_selected_municipality.val()
      self.init()
    }

    self.click_municipality = function(municipality_id){
      input_selected_municipality.val(municipality_id);
    }

    self.drawChart = function(chart_data) {

      // charts
      var cats = []
      var vals = []
      var medium_breakdown = chart_data.medium_breakdown;

      for (var medium in medium_breakdown) {
        if (medium_breakdown.hasOwnProperty(medium)) {
          cats.push(medium);
          vals.push(medium_breakdown[medium]);
        }
      }

      $('.chart-media-coverage').highcharts({
        chart: {
          type: 'column'
        },
        title: {
          text: '',
          style: {
            display: 'none'
          }
        },
        subtitle: {
          text: '',
          style: {
            display: 'none'
          }
        },
        xAxis: {
          categories: cats,
          labels: {
            step: 1,
            formatter: function(v) {
              if (this.value.length > 15) {
                return this.value.slice(0, 15) + "...";
              } else {
                return this.value;
              }
            }
          }
        },
        yAxis: {
          title: {
            text: 'number of stories'
          }
        },
        series: [{
          showInLegend: false,
          data: vals
        }],
      });
    }
  };

})(jQuery, window);

$(function() {
  var coverage_view = new Dexter.CoverageView
  coverage_view.init()
});