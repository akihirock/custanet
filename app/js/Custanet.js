(function(){
	var debugStr;
	debugStr = 'http://custanets.appspot.com/';
	//debugStr = 'http://localhost:11080/';

	var g=window.document,
		a=g.createElement('script'),
		b=g.createElement('script'),
		d=false,
		e=g.createElement('div'),
		f=g.createTextNode('Custanet\nloading...'),
		h=e.style,i='https://ajax.googleapis.com/ajax/libs/',
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
		a.setAttribute('src',i+'jquery/1.9.0/jquery.min.js');
		j.item(0).appendChild(a);
		b.setAttribute('src',i+'jqueryui/1.10.0/jquery-ui.min.js');
		j.item(0).appendChild(b);
		
		
		a.onload=a.onreadystatechange=function(){
			if(!this.readyState||this.readyState=='loaded'||this.readyState=='complete'){
				b.onload=b.onreadystatechange=function(){
					if(!this.readyState||this.readyState=='loaded'||this.readyState=='complete'){
						if(!d){
							
							
							var c=g.createElement('script');
						    d=encodeURI(location.href);
							c.src=debugStr + 'login?url='+d.replace("#","'''");
							j.item(0).appendChild(c);
							d=true;
							
							
						}
					}
				};
			}
		};
	}
)();