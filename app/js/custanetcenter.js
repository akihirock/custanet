		$(function(){


		var cnt = $("#displayCount").val();
		
		var cntFunc = function(cnt){
			var str='';
			if ( ccnsLen/cnt > 1 ){
				for(var i=0,imax=ccnsLen/cnt;i<imax;i++){
					str = str + '<li class="page" data-page="' +  (i+1) + '"><a href="#">' +  (i+1)  + '</a></li>';
				}
				$(".pagination").html(str);
			}
		}
		cntFunc(cnt);
				
		var showPage = function(p){
			var start = (p -1 ) * cnt;
			var end = (p) * cnt;
			$("#custanetTable tbody tr").hide().slice(start,end).show();
			$(".pagination li").removeClass("active");
			$("li[data-page=" + p + "]").addClass("active");
			
			$("#ppn,#npn").remove();
			
			if( ( ccnsLen >0 && p != Math.ceil(ccnsLen/cnt))   ){
				$(".pagination").append('<li id="npn"><a href="#">&raquo;</a></li>');
			}
			
			if( (p != 1) ){
				$(".pagination").prepend('<li id="ppn"><a href="#">&laquo;</a></li>');
			}
		}
		showPage(1);
		
		$(document).on('click','.page',function(){
			var ac = $(this).data("page");
			showPage(ac);
		});

		$(document).on('click','#ppn',function(){
			var ac = $(".active").data("page") - 1;
			showPage(ac);
		});
		
		$(document).on('click','#npn',function(){
			var ac = $(".active").data("page") + 1;
			showPage(ac);
		});
		
		$("#displayCount").change(function () {
			cnt = $("#displayCount").val();
			showPage(1);
		});		
		
		if( ccnsLen <=  cnt){
			$("ul.pagination").hide();
		}else{
			for(var i=1;i<Math.floor(ccnsLen/cnt);i++){
				$("fpn").after('<li><a href="#">' + (i+1) + '</a></li>');
			}
		}
		
		var approvalShow = function(invitation){
			var str=""
			for( var i in invitation ){
				str += "<li><input class='invitation' type='checkbox' value='" + invitation[i] + "'><span>" + i + "</span></li>";
			}
			if(str!=""){
				$("#approvalArea").html("<h3>friend request approval</h3><ul>"+str+"</ul>");
				$("#approveFriend").show();
			}
		}

		var friendShow = function(friend){
			var str="",wrk="";
			for( var i in friend ){
				str += "<li><input class='friend' type='checkbox' value='" + friend[i] + "'><span>" + i + "</span></li>";
			}
			if(str!=""){
				$("#friendsArea").html("<h3>your friends</h3><ul>"+str+"</ul>");

				//group
				wrk = "<li><input class='group' type='checkbox' value='" + wrk.slice(0, wrk.length-1) + "' gname='all'><span>all</span></li>" ;
				for( var i in group ){
				   wrk += "<li><input class='group' type='checkbox' value='" + group[i] + "' gname='" + i + "'><span>" + i + "</span></li>";
				}
				wrk = "<ul>" + wrk + "</ul>" ;
				$("#groupsArea").html(wrk);
				$("#requestFriend,#deleteFriend,#deleteGroup").show();

			}
		}

		$("#request-btn").click(function(){
	        var onError = function (jqXHR, textStatus, errorThrown){
	        	$("#email").val("");
	        	$("#friendrequestsended").text("error").hide(3000);
	        	$("#request-btn").attr("disabled",false);
	        }	
	        var onSuccess = function (data, textStatus, jqXHR) 
	        {
	        	$("#email").val("");
	        	$("#friendrequestsended").hide(3000);
	        	$("#request-btn").attr("disabled",false);
	        };
	        $("#request-btn").attr("disabled",true);
	        $("#friendrequestsended").text("friend request sended").show();
			var cn = [{name:"email",value:$("#email").val()}];
	        $.ajax({
	            url : '/request', type : 'post', data : cn
	        }).success(onSuccess);
		});

		$("input.friend-check").change(function(){
			if( $("input.friend-check:checked").size()>0 ){
				$("#delete-btn").show();
			}else{
				$("#delete-btn").hide();
			}		
		});
		
		var checkFriend = function(data){
	        	var str = "";
	        	data = JSON.parse(data);
	        	for (d in data){
	        		str += '<label class="checkbox"><input class="friend-check" value="' + data[d].id + '" type="checkbox">' +  data[d].nam + '</label>';
	        		$("input.invitation[value='" + data[d].id + "']").parent("label").remove();
	        	}
	        	if ( $("input.invitation").size() == 0 ){
	        		$("#left-pannel-invitation").remove();
	        	}
	        	$("#left-pannel-friends").html(str);	
		}
			
		$("#invite-btn").click(function(){
	        var onError = function (jqXHR, textStatus, errorThrown){
	        	$("#invite-btn").attr("disabled",false);
	        	$("#invitebtnmsg").text("error").hide(3000);
	        }
	        var onSuccess = function (data, textStatus, jqXHR) 
	        {
	        	$("#invite-btn").attr("disabled",false);
	        	$("#invitebtnmsg").hide(3000);
	        	checkFriend(data);
	        };
			$("#invite-btn").attr("disabled",true);
	        $("#invitebtnmsg").text("Invited").show();
	        var cn = [];
	        $("input.invitation:checked").each(function(){
	       		cn.push({name:"fid",value:$(this).val()});
	        });
	        $.ajax({
	            url : '/invite', type : 'post', data : cn
	        }).success(onSuccess).error(onError);
		});

		$("#delete-btn").click(function(){
	        var onSuccess = function (data, textStatus, jqXHR) 
	        {
				checkFriend(data);
	        };
	        
	        var cn = [];
	        $("input.friend-check:checked").each(function(){
	       		cn.push({name:"fid",value:$(this).val()});
	        });
	        $.ajax({
	            url : '/delete', type : 'post', data : cn
	        }).success(onSuccess);
		});
		
			
		$("#allcnts").click(function(){
			if( $(this).is(':checked') ){
				$("#custanetTable tbody td input:visible").prop("checked", true);
			}else{
				$("#custanetTable tbody td input:visible").prop("checked", false);
			}
		});
		
		
		$("[name=custanet-list]").change(function(){
			if($("[name=custanet-list]:checked").size()==0){
				$("#delete-cn-btn").attr("disabled","disabled");
			}else{
				$("#delete-cn-btn").removeAttr("disabled");
			}
		});
		
		$("#delete-cn-btn").click(function(){
	        var onSuccess = function (data, textStatus, jqXHR) 
	        {
	        	data = JSON.parse(data);
	        	for (var i=0,imax=data.length;i<imax;i++) {
		        	for (var j=0,jmax=ccns.length;j<jmax;j++) {
	        		　　if(ccns[j].key==data[i]){
	        				ccns.splice(j, 1);
	        				j=jmax+1;
	        		　　}
		        	}
	        	}
	        	
	        	var scope = angular.element( $("#main-pannel") ).scope();
	        	scope.$apply();
	        	
	        	
	        };
	        
	        var cn = [];
	        $("[name=custanet-list]:checked").each(function(){
	       		cn.push({name:"cid",value:$(this).val()});
	        });
	        $.ajax({
	            url : '/deleteCn', type : 'post', data : cn
	        }).success(onSuccess);
		});		
		
		
		
		// クッキー保存　setCookie(クッキー名, クッキーの値, クッキーの有効日数); //
		function setCookie(c_name,value,expiredays){
		    // pathの指定
		    var path = location.pathname;
		    // pathをフォルダ毎に指定する場合のIE対策
		    var paths = new Array();
		    paths = path.split("/");
		    if(paths[paths.length-1] != ""){
		        paths[paths.length-1] = "";
		        path = paths.join("/");
		    }
		    // 有効期限の日付
		    var extime = new Date().getTime();
		    var cltime = new Date(extime + (60*60*24*1000*expiredays));
		    var exdate = cltime.toUTCString();
		    // クッキーに保存する文字列を生成
		    var s="";
		    s += c_name +"="+ escape(value);// 値はエンコードしておく
		    s += "; path="+ path;
		    if(expiredays){
		        s += "; expires=" +exdate+"; ";
		    }else{
		        s += "; ";
		    }
		    // クッキーに保存
		    document.cookie=s;
		}
		
		function getCookie(c_name){
		    var st="";
		    var ed="";
		    if(document.cookie.length>0){
		        // クッキーの値を取り出す
		        st=document.cookie.indexOf(c_name + "=");
		        if(st!=-1){
		            st=st+c_name.length+1;
		            ed=document.cookie.indexOf(";",st);
		            if(ed==-1) ed=document.cookie.length;
		            // 値をデコードして返す
		            return unescape(document.cookie.substring(st,ed));
		        }
		    }
		    return "";
		}	
		
		setCookie('cuser',"{{cuserKey}}",1);
		
		
	  	$("#twin").click(function(){
			window.open("<%=debugStr %>/twSignout","aaa");	
		});		


		$("#twout").click(function(){
			window.open("<%=debugStr %>/twSignIn","bbb");
		});			

		
		$("#nickBtn").click(function(){
			var nickname = $("#nickname").val();
      		if(nickname!=""){
  				var cn = [
						{name:"nickname",value:nickname}
				];
				var onSuccess = function(data, textStatus, jqXHR) 
                {
					location.reload(true);
                };	
				var onError = function (data, textStatus, jqXHR){
					$("#nickErr").html("Please input another nickname");
				};		
				$.ajax({
        			url : "/signin", type : 'post', data :cn
    			}).success(onSuccess).error(onError);	
    			return false;
			}  					
		});			
		
		$("#nick-btn").click(function(){
			var nickname = $("#nick-txt").val();
      		if(nickname!=""){
  				var cn = [
						{name:"action",value:"nick"},
						{name:"nick",value:nickname}
				];
				var onSuccess = function(data, textStatus, jqXHR) 
                {
                    if(data["status"].indexOf("ok")!=-1){
						location.reload(true);
					}else{
						$("#nick-err").html("Please input another nickname");
					}
                };	
				var onError = function (data, textStatus, jqXHR){
					$("#nick-err").html("Please input another nickname");
				};		
				$.ajax({
        			url : debugStr + "/user", type : 'post', data :cn
    			}).success(onSuccess).error(onError);	
    			return false;
			}  					
		});	
		
		
		
		
		
		
		
	});  
	  	
	
	
	
		
