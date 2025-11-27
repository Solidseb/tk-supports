// --------------------------------------------------------------------
// Author  : mashimonator
// Create  : 2009/01/08
// Update  : 2009/01/14
// Description : ブラウザ判定をして、対応していればお気に入りに登録する
// --------------------------------------------------------------------

function bookmark(){

	var userSystem = new browserInfo.get(navigator.userAgent);
	var name = document.title;
	var url = window.location.href;

	var browser = userSystem.browserShortName;
	var version = parseFloat(userSystem.browserVersion);

	if ( browser == "ie" && version >= 4 ) {
		// IE4 以上
		window.external.AddFavorite(url,name);
	} else if ( browser == "ff" ) {
		// Firefox
		window.sidebar.addPanel(name,url,'');
	} else {
		// その他
		alert('「Ctrl(command)」キー + 「D」でお気に入りに追加してください！');
		return;
	}

}

var browserInfo = {

	get : function() {

		var key, index, keyIndex, keyIndexEnd, versionKey, i, j;
		var uaString = navigator.userAgent.toUpperCase();

		this.browserLongName = "---";
		this.browserShortName = "---";
		this.browserVersion = "---";

		var BROWSERS = new Object();
		BROWSERS['MZ'] = new setBrowser('Mozilla','mz','GECKO');
		BROWSERS['IE'] = new setBrowser('Internet Explorer','ie','MSIE');
		BROWSERS['AO'] = new setBrowser('AOL','ao','AOL');
		BROWSERS['SF'] = new setBrowser('Safari','sf','SAFARI');
		BROWSERS['OP'] = new setBrowser('Opera','op','OPERA');
		BROWSERS['OW'] = new setBrowser('OmniWeb','ow','OMNIWEB');
		BROWSERS['IC'] = new setBrowser('iCab','ic','ICAB');
		BROWSERS['NS'] = new setBrowser('Netscape','ns','NETSCAPE,NETSCAPE6');
		BROWSERS['NN'] = new setBrowser('Netscape Navigator','nn','MOZILLA');
		BROWSERS['FF'] = new setBrowser('Firefox','ff','FIREFOX');


		var UNIXDETAIL = new Array("LNX","BSD");
		var checkVersionExp01 = new Array(' ', '/', '-', '');
		var checkVersionExp02 = new Array(';', ' ', '(', '[', ')', '+', '-', '/');

		uaString = " " + uaString + ";";
		

		index = 0;
		for (key in BROWSERS) {
			for (i=0; i<BROWSERS[key].keyword.length; i++) {
				keyIndex = uaString.indexOf(BROWSERS[key].keyword[i].toUpperCase());
				if (keyIndex > index) {
					this.browserLongName = BROWSERS[key].longName;
					this.browserShortName = BROWSERS[key].shortName;
					versionKey = BROWSERS[key].keyword[i].toUpperCase();
					index = keyIndex;
				}
			}
		}

		// Navigator is reary?
		if (this.browserShortName == "nn" && uaString.indexOf("COMPATIBLE")>0) {
			this.browserLongName = "---";
			this.browserShortName = "---";
		}

		// Version Check
		if (this.browserLongName != "---") {
			for (i=0; i<checkVersionExp01.length; i++) {
				key = versionKey + checkVersionExp01[i];
				if ( ( keyIndex = uaString.indexOf(key) ) > 0 ) break;
			}
			// Mozilla
			if ( key == 'GECKO/' ) {
				key = 'RV:';
				keyIndex = uaString.indexOf(key);
			}
			keyIndex = keyIndex + key.length;
			index = uaString.length;
			for (i=0; i<checkVersionExp02.length; i++) {
				if ((key = uaString.indexOf(checkVersionExp02[i], keyIndex)) > 0) {
					if (key < index) {
						keyIndexEnd = key;
						index = keyIndexEnd;
					}
				}
			}
			this.browserVersion = uaString.substring(keyIndex, keyIndexEnd);
		}

		function setBrowser(longName,shortName,keyWord) {
			this.longName = longName;
			this.shortName = shortName;
			this.keyword = keyWord.split(",");
		}

	}

}



