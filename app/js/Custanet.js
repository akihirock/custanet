(function(){
	
	var z = document.getElementById("custanet-loading");
	if (z==null){
	
		var debugStr;
		debugStr = 'https://custanets.appspot.com/';
		debugStr = 'http://localhost:11080/';
	
		var g=window.document,
			a=g.createElement('script'),
			b=g.createElement('script'),
			d=encodeURI(location.href),
			e=g.createElement('div'),
			f=g.createTextNode('Custanet\nloading...'),
			h=e.style,
			j=g.getElementsByTagName('head');
			e.id='custanet-loading';
			e.style.textShadow = "1px 1px 15px red";
			e.style.color="blue";
			e.appendChild(f);
			h.top='30%';
			h.zIndex=99999;
			h.fontSize='70pt';
			h.position='fixed';
			h.textAlign="center";
			h.width='100%';
			document.body.appendChild(e);
			var c=g.createElement('script');
			c.src=debugStr + 'login?url='+d.replace("#","'''");
			j.item(0).appendChild(c);	
	}		
})();