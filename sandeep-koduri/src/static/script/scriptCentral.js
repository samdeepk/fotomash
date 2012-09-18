loginArea={
		showLogin:function(){
			
			$(".LoginPop").toggle()
			
		},
		hideLogin:function(){
			
			$(".LoginPop").hide()
			
		}
		
		
}


AdvanceSearch={
		show:function(){
			
			$(".AdvSrchOptions").toggle()
			
		},
		hide:function(){
			
			$(".AdvSrchOptions").hide()
			
		},
		searchListCount:0,
		searchListCountFetched:0,
		topSearchList : [],
		search:function(){
			keyWord = $('.SrcBx').val()
			if (keyWord.length==0){return}
			AdvanceSearch.hide()
			loginArea.hideLogin()
			
			
			AdvanceSearch.searchListCount=0
			AdvanceSearch.searchListCountFetched=0
			AdvanceSearch.topSearchList=[]
			$('.HomeCenBg').addClass("noBG")
			$(".HmSrchArea").addClass("HmSrchAreaInTop")
			$(".HomeHero").hide()
			$(".SrcRstDis .result").html("")
			$(".SrcRstDis").show()
			$(".SrchBtn img").attr('src','/static/images/innsrchbtn.png')
			
				dataSearch = {}
				
				dataSearch["keyword"] = keyWord
				dataSearch['categories']=$("#categories").val();
				listDomains = $(".SrcOpt input:checked")
				AdvanceSearch.searchListCount = listDomains.length
				if(AdvanceSearch.searchListCount==0){
					dataSearch["domains"] = "flickr"
					AdvanceSearch.disopatchSearch(dataSearch);
					AdvanceSearch.searchListCount =1;
					return;
				}
				listDomains.each(function(){
					dataSearch["domains"] = $(this).val()
					if (dataSearch["domains"].length>0 ){
						AdvanceSearch.disopatchSearch(dataSearch)
					}
				})
			
				
			
			
				
			
		},
		updateUserSearchHistory:function(keyWrd,toplist){
			$('#SearchHistory').val()
			
			var request = $.ajax({
				  url: "/searchTrack",
				  type: "POST",
				  data:{'Search':keyWrd,"SearchHistory":$("#SearchHistory").val(),'topList':JSON.stringify(toplist)},
				  dataType: "json",
				  success: function(data) {
					  		
						  }
				});
		},
		disopatchSearch:function(sata){
			
				var request = $.ajax({
				  url: "/search",
				  type: "POST",
				  data:sata,
				  dataType: "json",
				  success: function(data) {
					  		//console.log(data)
					  		
					  		$.each(data['results'], function(index, value) { 
							  AdvanceSearch.populateSearchArea(value,sata['keyword'],data["source"],index)
							});
					  		AdvanceSearch.searchListCountFetched = AdvanceSearch.searchListCountFetched+1
					  		if(data['results'].length>0){ AdvanceSearch.topSearchList.push(data['results'][0])}
					  		if(AdvanceSearch.searchListCountFetched == AdvanceSearch.searchListCount )
					  			{
					  				AdvanceSearch.updateUserSearchHistory(keyWord,AdvanceSearch.topSearchList)
					  				
					  			}
						  }
				});

				/*request.done(function(msg) {
				  
				});

				request.fail(function(jqXHR, textStatus) {
				  console.log( "Request failed: " + textStatus );
				});*/
		},
		populateSearchArea:function(img,keyword,domain,index){
			
			Indata = '<div class="order'+index+' res"><div class="testIt"></div><a target="_blank" href="'+img['refURL']+'" rel="example1" title="" class="cboxElement">'+img['title']+'<img src="'+img['imagePath']+'"><br> </a></div>'
			inrows = $(".order"+index)
			if(inrows.length>0){
				$(".order"+index+":last").after(Indata)
			}
			else{$(".SrcRstDis .result").append(Indata);}
			
		}
		

}