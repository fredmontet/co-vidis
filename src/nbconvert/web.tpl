{%- extends 'full.tpl' -%}

<!DOCTYPE html>
<html>
<head>
{%- block header -%}
<meta charset="utf-8" />
<title>{{resources['metadata']['name']}}</title>

<script src="https://cdnjs.cloudflare.com/ajax/libs/require.js/2.1.10/require.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/2.0.3/jquery.min.js"></script>

{% for css in resources.inlining.css -%}
    <style type="text/css">
    {{ css }}
    </style>
{% endfor %}

<!-- Can put analytics code here, if desired -->

<style type="text/css">
/* Overrides of notebook CSS for static HTML export */
body {
  overflow: visible;
  padding: 8px;
}
div#notebook {
  overflow: visible;
  border-top: none;
}
@media print {
  div.cell {
    display: block;
    page-break-inside: avoid;
  } 
  div.output_wrapper { 
    display: block;
    page-break-inside: avoid; 
  }
  div.output { 
    display: block;
    page-break-inside: avoid; 
  }
}
    
div#notebook{
  margin-top:50px;
  margin-bottom:100px;
}

div.cell{
  max-width:60em;
  margin-left:auto;
  margin-right:auto;

}

div.input_prompt, div.output_prompt{
  margin-left:-11ex;
}

div.input, div.output_wrapper{
  margin-top:1em;
  margin-bottom:1em;
}
    
div.text_cell{
  margin-top:-2px;
  margin-bottom:-2px;
  padding-top:2px;
  padding-bottom:2px;
  border-left:2px solid #505050;
  border-collapse:collapse;
  border-top:none;
  border-bottom:none;
}


{%- endblock header -%}
</head>


<body>
{% block body %}
  <div tabindex="-1" id="notebook" class="border-box-sizing">
    <div class="container" id="notebook-container">
      {{ super() }}
      <div class="cell border-box-sizing text_cell rendered">
        <div class="prompt input_prompt">
	      </div>
      </div>
    </div>
  </div>
{%- endblock body %}
</body>


{% block footer %}
</html>
{% endblock footer %}