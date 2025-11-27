#############################################################
#
# WebCalenderC3 version 0.32
#
# 履　歴：
# Ver 0.30  04.02.08 WebCalender2を改造しWebCalenderC3として公開
# Ver 0.31  04.12.02 月表示や携帯表示で開始時間を表示するように変更
#                    携帯表示の▲が見にくいため↑に変更
# Ver 0.32  08.11.19 Softback携帯でPC版が表示されてしまう問題を修正
# Ver 0.32s 09.03.24 セキュリティ強化のため入力パラメータチェックを追加
#
# -----------------------------------------------------------
# オリジナル情報 - WebCalender2
# 制作者： Nobuaki Ueno
# version： 0.22
# 制作日： 02.03.10
# 種類： フリーウエア
# 動作確認： FreeBSD4.1Release + Perl5.005_03
#
# -----------------------------------------------------------
# オリジナル情報 - WebCalender
# 制作者： Koji Onishi
# 制作日： 98.10.15
# 種類： フリーウエア
# 動作確認： FreeBSD & perl5
#
############################################################

##########################################################
# ★★★メイン★★★
sub main{

&lib'getinputfromweb($kanji_code);

$form = $form{'form'};		#1:月、2:縦、その他:年、i:imode
$wyear = $form{'year'};
$wmon = $form{'mon'};

($year,$mon,$day,$wday,$hour,$min,$sec) = &lib'getdatetime(time);

#デフォルトの年と月
if($wyear eq ""){
	#デフォルト年を強制設定
	if ($default_year eq ""){
		$wyear = $year;
		if (($form==0)&&($nendo_mode)) {
			if ($mon < $nendo_start) {$wyear = $year -1;}
		}
	}else{
		$wyear = $default_year;
	}
}
if($wmon eq ""){
	$wmon = $mon;
}

#入力チェック for Secure version add by mi
if ($wyear =~ /^[0-9]{4}$/){
}else{
	$wyear = $year;
}
if ($wmon =~ /^[0-9]{1,2}$/){
}else{
	$wmon = $mon;
}



$yprevyear=$wyear-1;
$ynextyear=$wyear+1;

#月表示、次の年月、前の年月
$prevyear=$wyear;
$nextyear=$wyear;
$prevmon=$wmon-1;
$nextmon=$wmon+1;
if ($prevmon <= 0) {
	$prevyear = $prevyear-1;
	$prevmon = 12;
}
if ($nextmon >= 13) {
	$nextyear = $nextyear+1;
	$nextmon = 1;
}


#タイトル
$title="$wyear年カレンダー";
if ($nendo_mode) {$title="$wyear年度カレンダー";}
if ($y_title ne "") {$title = "$y_title";}

#携帯タイプの判断
$agent = $ENV{'HTTP_USER_AGENT'};
if($form{'form'} eq "i" || $agent =~ "DoCoMo" || $agent =~ "J-PHONE" || $agent =~ "SoftBank" || $agent =~ "KDDI"){
	if($form{'c'} eq ""){
		#携帯端末の画面表示桁設定
		#Docomo
		if($agent =~ "DoCoMo"){
			#１０桁表示機種
			if($agent =~ "N50" ||
			   $agent =~ "N821i" ||
			   $agent =~ "P821i" ||
			   $agent =~ "ER209" ||
			   $agent =~ "F671i" ||
			   $agent =~ "F503i" ||
			   $agent =~ "N210i" ||
			   $agent =~ "N211i" ||
			   $agent =~ "N200" ||
			   $agent =~ "P2101V"){
				$text_size = 16;
			#１２桁表示機種
			}elsif($agent =~ "F503iS" ||
			       $agent =~ "P211i" ||
			       $agent =~ "P503i" ){
				$text_size = 20;
			#その他８桁表示機種
			}else{
				$text_size = 12;
			}
		#J-SKY
		}elsif($agent =~ "J-PHONE"){
			#８桁表示機種
			if($agent =~ "J-SH02" ||
			   $agent =~ "J-DN02" ||
			   $agent =~ "J-P02" ||
			   $agent =~ "J-SH03" ||
			   $agent =~ "J-T04" ||
			   $agent =~ "J-SH04"||
			   $agent =~ "J-SH04B" ||
			   $agent =~ "J-P03" ||
			   $agent =~ "J-SH06" ){
				$text_size = 12;
			#１１桁表示機種
			}elsif($agent =~ "J-D05" ||
			       $agent =~ "J-D31" ){
				$text_size = 18;
			#その他１０桁表示機種
			}else{
				$text_size = 16;
			}
		#au cdmaOne C5000/3000
		}elsif($agent =~ "KDDI"){
			$text_size = 16;
		}else{
			$text_size = 12;
		}
	#表示桁引数指定の場合
	}else{
	 	$text_size = ($form{'c'} - 2) * 2;
	}

	$imode = "1";
	$form = "i";
}

# 表示形式の指定がない場合はデフォルトの表示形式
if ($form eq ""){ $form=$default_form; }

#----------
# imode
#----------
if($imode){
	&html_head_imode;			#HTML先頭部分imode用
	$title="$wyear年$wmon月";
	if ($m_title ne "") {$title = "$m_title";}
	print "<div align=\"center\">";
	print "$title<br>";
	print "[<a href=\"webcalc3.cgi?form=i&year=$prevyear&mon=$prevmon\">prev</a>]";
	print "&nbsp;";
	print "[<a href=\"webcalc3.cgi?form=i&year=$nextyear&mon=$nextmon\">next</a>]<br>";
	print "</div>";
	&html_body_imode;
	if ($backlink_i ne ""){
		print "[<a href=\"$backlink_i\">$backmsg_i</a>]\n";
	}

#----------
# 縦表示
#----------
}elsif ($form eq "2") {
	&html_head;			#HTML先頭部分

	$body ="<BODY";
	# 背景
	if ($body_bgcolor ne "") {$body="$body bgcolor=\"$body_bgcolor\"";}
	if ($body_bgimage ne "") {$body="$body background=\"$body_bgimage\"";}
	print "$body>";
	print "<div align=\"center\">";

	$title="$wyear年$wmon月";
	if ($m_title ne "") {$title = "$m_title";}
	print "<H1 class=\"yyyy\">$title</H1>";
	# ヘッダー
	if ($m_header ne "") {
		print "$m_header<br>";
	}
	print "[<a href=\"webcalc3.cgi?form=2&year=$prevyear&mon=$prevmon\">prev</a>]";
	print "&nbsp;";
	$this_year = $wyear;
	if (($nendo_mode)&&($wmon < $nendo_start)) { $this_year -= 1;}
	print "[<a href=\"webcalc3.cgi?form=0&year=$this_year\">年</a>]";
	print "&nbsp;";
	print "[<a href=\"webcalc3.cgi?form=2&year=$nextyear&mon=$nextmon\">next</a>]<br>";
	print "[<a href=\"webcalc3.cgi?form=1&year=$wyear&mon=$wmon\">標準</a>]<br><br>";
	&html_body_tate;
	# フッター
	if ($m_footer ne ""){
		print "<TABLE  height=\"50\" width=\"640\" BORDER=0 CELLPADDING=1 CELLSPACING=1>\n";
		print "<TR><TD colspan=\"2\" align=\"center\">$m_footer</TD></TR>\n";
		print "</TABLE>\n";
	}
	if ($backlink ne ""){
		print "<TABLE  height=\"50\" width=\"640\" BORDER=0 CELLPADDING=1 CELLSPACING=1>\n";
		print "<TR><TD colspan=\"2\" align=\"right\"><a href=\"$backlink\">$backmsg</a></TD></TR>\n";
		print "</TABLE>\n";
	}

#----------
# 月表示
#----------
}elsif($form eq "1"){
	&html_head;			#HTML先頭部分

	$body ="<BODY";
	# 背景
	if ($body_bgcolor ne "") {$body="$body bgcolor=\"$body_bgcolor\"";}
	if ($body_bgimage ne "") {$body="$body background=\"$body_bgimage\"";}
	print "$body>";
	print "<div align=\"center\">";

	$mstyle=int($wmon/4)+1;
	$title="$wyear年$wmon月";
	if ($m_title ne "") {$title = "$m_title";}
	print "<H1 class=\"yyyy\">$title</H1>";
	# ヘッダー
	if ($m_header ne "") {
		print "$m_header<br>";
	}
	print "[<a href=\"webcalc3.cgi?form=1&year=$prevyear&mon=$prevmon\">prev</a>]";
	print "&nbsp;";
	$this_year = $wyear;
	if (($nendo_mode)&&($wmon < $nendo_start)) { $this_year -= 1;}
	print "[<a href=\"webcalc3.cgi?form=0&year=$this_year\">年</a>]";
	print "&nbsp;";
	print "[<a href=\"webcalc3.cgi?form=1&year=$nextyear&mon=$nextmon\">next</a>]<br>";
	print "[<a href=\"webcalc3.cgi?form=2&year=$wyear&mon=$wmon\">縦型</a>]<br><br>";
	&html_body_1mon;

	# フッター
	$footer_width = $day_width * 7 + 40;
	if ($m_footer ne ""){
		print "<TABLE  height=\"50\" width=\"$footer_width\" BORDER=0 CELLPADDING=1 CELLSPACING=1>\n";
		print "<TR><TD colspan=\"2\" align=\"center\">$m_footer</TD></TR>\n";
		print "</TABLE>\n";
	}
	if ($backlink ne ""){
		print "<TABLE  height=\"50\" width=\"$footer_width\" BORDER=0 CELLPADDING=1 CELLSPACING=1>\n";
		print "<TR><TD colspan=\"2\" align=\"right\"><a href=\"$backlink\">$backmsg</a></TD></TR>\n";
		print "</TABLE>\n";
	}

#----------
# 年表示
#----------
}else{
	&html_head;			#HTML先頭部分

	$body ="<BODY";
	# 背景
	if ($body_bgcolor ne "") {$body="$body bgcolor=\"$body_bgcolor\"";}
	if ($body_bgimage ne "") {$body="$body background=\"$body_bgimage\"";}
	print "$body>";
	print "<div align=\"center\">";
	print "<H1 class=\"yyyy\">$title</H1>";

	# ヘッダー
	if ($y_header ne "") {
		print "$y_header<br>";
	}

	# [prev][next]
	if ($year_navi) {
		print "[<a href=\"webcalc3.cgi?form=0&year=$yprevyear\">prev</a>]";
		print "&nbsp;";
		$this_year = $year;
		if (($nendo_mode)&&($mon < $nendo_start)) { $this_year -= 1;}
		print "[<a href=\"webcalc3.cgi?form=0&year=$this_year\">今年</a>]";
		print "&nbsp;";
		print "[<a href=\"webcalc3.cgi?form=0&year=$ynextyear\">next</a>]<br>";
	}

	# レイアウト用
	print "<TABLE BORDER=0 CELLPADDING=10 CELLSPACING=0>";
	print "<TR><TD>\n";

	#
	# カレンダー、1月から12月までループ、3ヶ月ごとに改行
	#
	print "<Table BORDER=0 CELLPADDING=10 CELLSPACING=0>";
	$mstyle=1;	#見出しの色
	for($im = 1; $im <= 12; $im++){
		$wyearorg = $wyear;
		$wmon = $im;
		if ($nendo_mode) {
			# 年度開始月から順に表示、12月を過ぎたら翌年1月から表示
			if ($im + $nendo_start -1 > 12) {
				$nendo_start -= 12;
				$wyear = $wyearorg + 1;
			}
			$wmon = $im + $nendo_start - 1;
		}
		if ($im % 3 == 1) {print "<tr>\n"}
		print "<td valign=\"top\">";
		&html_body_12mon;
		print "</td>\n";
		if ($im % 3 == 0) {
			$mstyle+=1;
			print "</tr>\n"
		}
	}
	print "</Table>\n";

	print "</TD><TD valign=\"top\">\n";

	# 凡例
		print "<br>\n";
		print "<table border=0>\n";
		$i = $shu_num-1;
		while($i > 0){
			print "<tr><td>";
			print "<table border=1><tr><td width=\"10\" class=\"nor\" bgcolor=\"$shu_color[$i]\">$zen_space</td></tr></table>\n";
			print "</td>";
			print "<td class=\"han\">";
			print "$shu[$i]\n";
			print "</td></tr>";

			$i--;
		}
		print "<tr><td colspan=\"2\">";
		print "<br>";
		print "<table border=1><tr><td width=\"100\" class=\"m1\">1</td></tr></table>\n";
		print "</td></tr>";
		print "<tr><td colspan=\"2\" class=\"han\">";
		print "クリックで詳細画面へ\n";
		print "</td></tr>";
		print "</table>\n";

	print "</TD></TR>\n";
	if ($y_footer ne ""){
		print "<TR><TD colspan=\"2\" align=\"center\">$y_footer</TD></TR>\n";
	}
	if ($backlink ne ""){
		print "<TR><TD colspan=\"2\" align=\"right\"><a href=\"$backlink\">$backmsg</a></TD></TR>\n";
	}
	print "</TABLE>";

}

print "</div></body></html>";	#HTML末尾部分

}
#
#####



############################################################
# ヘッダ
sub html_head
{
print "Content-type: text/html\n\n";
print qq(
<HTML>
<HEAD>
<TITLE>$title</TITLE>
<META HTTP-EQUIV="Cache-Control" CONTENT="no-cache">
<style>
.yyyy{ font-size:24px ; font-family:"verdana" ; text-decoration:none ; font-weight:bold ; text-align:center ; color: #000000} /* 見出し */
 /* 月見出し-年表\示 */
.m0{ font-size:10px ; font-family:"verdana" ; text-decoration:none ; font-weight:bold ;
				text-align:center ; color: #ffffff ; background-color: $obicolor0; }
.m1{ font-size:10px ; font-family:"verdana" ; text-decoration:none ; font-weight:bold ;
				text-align:center ; color: #ffffff ; background-color: $obicolor1; }
.m2{ font-size:10px ; font-family:"verdana" ; text-decoration:none ; font-weight:bold ;
				text-align:center ; color: #ffffff ; background-color: $obicolor2; }
.m3{ font-size:10px ; font-family:"verdana" ; text-decoration:none ; font-weight:bold ;
				text-align:center ; color: #ffffff ; background-color: $obicolor3; }
.m4{ font-size:10px ; font-family:"verdana" ; text-decoration:none ; font-weight:bold ;
				text-align:center ; color: #ffffff ; background-color: $obicolor4; }
 /* 月見出し-月表\示標準 */
.mL1{ font-size:18px ; font-family:"verdana" ; text-decoration:none ; font-weight:bold ;
				text-align:center ; color: #ffffff ; background-color: $obicolor1; }
.mL2{ font-size:18px ; font-family:"verdana" ; text-decoration:none ; font-weight:bold ;
				text-align:center ; color: #ffffff ; background-color: $obicolor2; }
.mL3{ font-size:18px ; font-family:"verdana" ; text-decoration:none ; font-weight:bold ;
				text-align:center ; color: #ffffff ; background-color: $obicolor3; }
.mL4{ font-size:18px ; font-family:"verdana" ; text-decoration:none ; font-weight:bold ;
				text-align:center ; color: #ffffff ; background-color: $obicolor4; }
 /* 月見出し-月表\示縦 */
.mT1{ font-size:12px ; font-family:"verdana" ; text-decoration:none ; font-weight:bold ;
				text-align:center ; color: #ffffff ; background-color: $obicolor1; }
.mT2{ font-size:12px ; font-family:"verdana" ; text-decoration:none ; font-weight:bold ;
				text-align:center ; color: #ffffff ; background-color: $obicolor2; }
.mT3{ font-size:12px ; font-family:"verdana" ; text-decoration:none ; font-weight:bold ;
				text-align:center ; color: #ffffff ; background-color: $obicolor3; }
.mT4{ font-size:12px ; font-family:"verdana" ; text-decoration:none ; font-weight:bold ;
				text-align:center ; color: #ffffff ; background-color: $obicolor4; }

.sun{ font-size:10px ; font-family:"verdana" ; text-decoration:none ; text-align:right ; color: $suncharcolor } /* 日曜 */
.sat{ font-size:10px ; font-family:"verdana" ; text-decoration:none ; text-align:right ; color: $satcharcolor } /* 土曜 */
.nor{ font-size:10px ; font-family:"verdana" ; text-decoration:none ; text-align:right ; color: $charcolor } /* 平日 */
.han{ font-size:10px ; font-family:"verdana" ; text-decoration:none ; text-align:left ; color: #000000 } /* 凡例 */
.today{ font-size:10px ; font-family:"verdana" ; text-decoration:none ; font-weight:bold ; text-align:right ; color: #000000 } /* 今日 */

.sunLT{ font-size:20px ; font-family:"verdana" ; text-decoration:none ; text-align:left ; vertical-align:top ; color: $suncharcolor } /* 日曜 */
.satLT{ font-size:20px ; font-family:"verdana" ; text-decoration:none ; text-align:left ; vertical-align:top ; color: $satcharcolor } /* 土曜 */
.norLT{ font-size:20px ; font-family:"verdana" ; text-decoration:none ; text-align:left ; vertical-align:top ; color: $charcolor } /* 平日 */
.sunL{ font-size:30px ; font-family:"verdana" ; text-decoration:none ; text-align:left ; vertical-align:top ; color: $suncharcolor } /* 日曜 */
.satL{ font-size:30px ; font-family:"verdana" ; text-decoration:none ; text-align:left ; vertical-align:top ; color: $satcharcolor } /* 土曜 */
.norL{ font-size:30px ; font-family:"verdana" ; text-decoration:none ; text-align:left ; vertical-align:top ; color: $charcolor } /* 平日 */
.rokuyoL{ font-size:8px ; text-decoration:none ; text-align:left ; vertical-align:top ; color: #000000 } /* 六曜 */

 /* セルの書式-月表\示標準 */
.schedL{ font-size:12px ; text-decoration:none ; text-align:left ; vertical-align:top ; color: #000000 ; width:$day_width}

.sunT{ font-size:12px ; font-family:"verdana" ; text-decoration:none ; text-align:right ; color: $suncharcolor } /* 日曜 */
.satT{ font-size:12px ; font-family:"verdana" ; text-decoration:none ; text-align:right ; color: $satcharcolor } /* 土曜 */
.norT{ font-size:12px ; font-family:"verdana" ; text-decoration:none ; text-align:right ; color: $charcolor } /* 平日 */

.schedTH{ font-size:12px ; text-decoration:none ; text-align:center ; color: #000000 } /* 時間 */
.schedT{ font-size:12px ; text-decoration:none ; text-align:left ; color: #000000 } /* スケジュール */
.schedTright{ font-size:12px ; text-decoration:none ; text-align:right ; color: #000000 } /* スケジュール */

</style>
</HEAD>
);

}
#
#####


############################################################
# ヘッダ
sub html_head_imode
{
print "Content-type: text/html\n\n";
print qq(
<HTML>
<HEAD>
<TITLE>webcalc3</TITLE>
<META HTTP-EQUIV="Cache-Control" CONTENT="no-cache">
</HEAD>
<BODY>
<div align="left">
);
}
#
#####



##########################################################
# カレンダーimode
sub html_body_imode
{

#月の第１週めの始めの曜日を求める
$startday = &lib'getyoubi($wyear,$wmon,1);

#第１日
$tama = 1;

#最終日
$tamaend = &lib'getgetumatu($wyear,$wmon);

# 繰返し処理
$yearlydata = "$datadir/yearly_$wyear\.dat";
@yearly = &lib'kurikaeshi_yearlyc3($yearlydata);

	while($tama <= $tamaend){
		$i = &lib'getyoubi($wyear,$wmon,$tama);
		($yearly_flag,@yearly_data) = &lib'getyearly("$wmon/$tama",@yearly);
		$flag = $yearly_flag;

		if ($tama == 1) {
			print "<div align=\"center\">";
			print "<a name=\"1\" href=\"#15d\">↓</a>";
			print "</div>";
		}

		if ($tama == 15) {
			print "<div align=\"center\">";
			print "<a name=\"15d\" href=\"#28\">↓</a>";
			print "$zen_space";
			print "<a name=\"15u\" href=\"#1\">↑</a>";
			print "</div>";
		}

		if ($tama == 28) {
			print "<div align=\"center\">";
			print "<a name=\"28\" href=\"#15u\">↑</a>";
			print "</div>";
		}

		print "$wmon/$tama";

		if($flag || $i == 0){
			print "<FONT COLOR=\"$t_suncolor\">";
		}
		print "$wdays[$i]";
		if($flag || $i == 0){
			print "</FONT>";
		}
		&disp_contents_i;
		$tama++;
	}
}
#
#####


##########################################################
# カレンダー本体1年分
sub html_body_12mon
{

#月の第１週めの始めの曜日を求める
$startday = &lib'getyoubi($wyear,$wmon,1);

#第１日
$tama = 1;

#最終日
$tamaend = &lib'getgetumatu($wyear,$wmon);

# 繰返し処理
$yearlydata = "$datadir/yearly_$wyear\.dat";
@yearly = &lib'kurikaeshi_yearlyc3($yearlydata);

	#月見出し
	print "<TABLE BORDER=1 CELLPADDING=1 CELLSPACING=1 BGCOLOR=#FFFFFF>\n";
	if (($wyear == $year)&&($wmon == $mon)) {
		print "<TR><TD colspan=7 class=\"m0\" align=\"center\">";	#今月
		print "<a class=\"m0\" href=\"webcalc3.cgi?form=1&year=$wyear&mon=$wmon\">";
	}else{
		print "<TR><TD colspan=7 class=\"m$mstyle\" align=\"center\">";
		print "<a class=\"m$mstyle\" href=\"webcalc3.cgi?form=1&year=$wyear&mon=$wmon\">";
	}
	print "＿＿＿＿＿";
	print "$wmon";
	print "＿＿＿＿＿";
	print "</a></TD></TR>\n";

	#曜見出し
	print "<TR>\n";
	for($i = 0; $i < 7; $i++){

		$youbi = $weekstart+$i;
		if($youbi > 6){$youbi = 0;}

		$weekday = @wdays[$youbi];

		if($i == (6 - $weekstart)){
			print "<TD class=\"sat\">";
		}elsif($i == (6 * $weekstart)){
			print "<TD class=\"sun\">";
		}else{
			print "<TD class=\"nor\">";
		}
		print "<P>$weekday</a>";
		print "</TD>\n";
	}
	print "</TR>";

	$startweek = 1;

	#月曜日スタート時
	if($weekstart == 1){
		if($startday == 0){
			$startday = 6;
		}else{
			$startday = $startday - $weekstart;
		}
	}
	while($tama <= $tamaend){
		print "<TR>\n";
		for($i = 0; $i < 7; $i++){

#			$youbi = &lib'getyoubi($wyear,$wmon,$tama);

			if($weekstart == 1){
				if($i != 6){
					$youbi = $i + 1;
				}else{
					$youbi = 0;
				}
			}else{
				$youbi = $i;
			}

			#もし第１週目ならば
			if($startweek == 1){
				if($i >= $startday){
					($yearly_flag,@yearly_data) = &lib'getyearly("$wmon/$tama",@yearly);
					$flag = $yearly_flag;

					#平日用style
					$class="nor";
					#もし土曜日ならば
					if($i == (6 - $weekstart)){
						$class="sat";
					#もし日曜日ならば
					}elsif($i == (6 * $weekstart)){
						$class="sun";
					}
					#祝日
					if($flag != 0){
						$class="sun";
					}
					#予定HTML
					&disp_contents12;
					#今日
					if("$wyear/$wmon/$tama" eq "$year/$mon/$day"){
						$btag_s="<b>";
						$btag_e="</b>";
					}else{
						$btag_s="";
						$btag_e="";
					}
					#TDタグ書き出し
					if ($bg ne ""){
						print "<TD class=\"$class\" bgcolor=\"$bg\">";
					}else{
						print "<TD class=\"$class\">";
					}
					print "$btag_s$tama$btag_e";
					print "</TD>\n";

					$tama++;
				}else{
					print "<TD class=\"nor\">\n";
					print "$w_jitaim_s$zen_space$w_jitaim_e<BR>";
					print "</TD>\n";
				}
			#もし第１週目でなければ
			}else{
				if($tama <= $tamaend){
					($yearly_flag,@yearly_data) = &lib'getyearly("$wmon/$tama",@yearly);
					($monthly_flag,@monthly_data) = &lib'getmonthly($tama,@monthly);
					($weekly_flag,@weekly_data) = &lib'getweekly($youbi,@weekly);
					$flag = $yearly_flag+$monthly_flag+$weekly_flag;

					#平日用style
					$class="nor";
					#もし土曜日ならば
					if($i == (6 - $weekstart)){
						$class="sat";
					#もし日曜日ならば
					}elsif($i == (6 * $weekstart)){
						$class="sun";
					}
					#祝日
					if($flag != 0){
						$class="sun";
					}
					#今日
					if("$wyear/$wmon/$tama" eq "$year/$mon/$day"){
						$btag_s="<b>";
						$btag_e="</b>";
					}else{
						$btag_s="";
						$btag_e="";
					}
					#予定HTML
					&disp_contents12;
					#TDタグ書き出し
					if ($bg ne ""){
						print "<TD class=\"$class\" bgcolor=\"$bg\">";
					}else{
						print "<TD class=\"$class\">";
					}
					print "$btag_s$tama$btag_e";
					print "</TD>\n";

					$tama++;
				}else{
					$tama++;
					print "<TD class=\"nor\">\n";
					print "$w_jitaim_s$zen_space$w_jitaim_e<BR>";
					print "</TD>\n";
				}
			}
		}
		print "</TR>\n";
		$startweek++;
	}
	print "</TABLE>\n";
}
#
#####


##########################################################
# カレンダー本体1月分
sub html_body_1mon
{

#月の第１週めの始めの曜日を求める
$startday = &lib'getyoubi($wyear,$wmon,1);

#第１日
$tama = 1;

#最終日
$tamaend = &lib'getgetumatu($wyear,$wmon);

# 繰返し処理
$yearlydata = "$datadir/yearly_$wyear\.dat";
@yearly = &lib'kurikaeshi_yearlyc3($yearlydata);

# 標準タイプ

	#月見出し
	$table_width = $day_width * 7 + 14;
	print "<TABLE BORDER=1 CELLPADDING=1 CELLSPACING=1 BGCOLOR=#FFFFFF width=$table_width>\n";
	print "<TR height=\"25\"><TD colspan=7 class=\"mL$mstyle\">$wmon</TD></TR>\n";			#月見出し
	print "<TR height=\"25\">\n";
	for($i = 0; $i < 7; $i++){

		$youbi = $weekstart+$i;
		if($youbi > 6){$youbi = 0;}

		$weekday = @wdays[$youbi];

		if($i == (6 - $weekstart)){
			print "<TD width=\"$day_width\" class=\"satLT\">";
		}elsif($i == (6 * $weekstart)){
			print "<TD width=\"$day_width\" class=\"sunLT\">";
		}else{
			print "<TD width=\"$day_width\" class=\"norLT\">";
		}
		print "<P>$weekday";
		print "</TD>\n";
	}
	print "</TR>";

	$startweek = 1;

	#月曜日スタート時
	if($weekstart == 1){
		if($startday == 0){
			$startday = 6;
		}else{
			$startday = $startday - $weekstart;
		}
	}
	while($tama <= $tamaend){
		print "<TR height=\"100\">\n";
		for($i = 0; $i < 7; $i++){

			if($weekstart == 1){
				if($i != 6){
					$youbi = $i + 1;
				}else{
					$youbi = 0;
				}
			}else{
				$youbi = $i;
			}

			#もし第１週目ならば
			if($startweek == 1){
				if($i >= $startday){
					($yearly_flag,@yearly_data) = &lib'getyearly("$wmon/$tama",@yearly);
					$flag = $yearly_flag;

					#平日用style
					$class="norL";
					#もし土曜日ならば
					if($i == (6 - $weekstart)){
						$class="satL";
					#もし日曜日ならば
					}elsif($i == (6 * $weekstart)){
						$class="sunL";
					}
					#祝日
					if($flag != 0){
						$class="sunL";
					}
					#TDタグ書き出し
					&disp_contents;

					$tama++;
				}else{
					print "<TD class=\"norL\">\n";
					print "$w_jitaim_s$zen_space$w_jitaim_e<BR>";
					print "</TD>\n";
				}
			#もし第１週目でなければ
			}else{
				if($tama <= $tamaend){
					($yearly_flag,@yearly_data) = &lib'getyearly("$wmon/$tama",@yearly);
					$flag = $yearly_flag;

					#平日用style
					$class="norL";
					#もし土曜日ならば
					if($i == (6 - $weekstart)){
						$class="satL";
					#もし日曜日ならば
					}elsif($i == (6 * $weekstart)){
						$class="sunL";
					}
					#祝日
					if($flag != 0){
						$class="sunL";
					}
					#今日
					if("$wyear/$wmon/$tama" eq "$year/$mon/$day"){
						$btag_s="<b>";
						$btag_e="</b>";
					}else{
						$btag_s="";
						$btag_e="";
					}
					#TDタグ書き出し
					&disp_contents;
					$tama++;
				}else{
					$tama++;
					print "<TD class=\"norL\">\n";
					print "$w_jitaim_s$zen_space$w_jitaim_e<BR>";
					print "</TD>\n";
				}
			}
		}
		print "</TR>\n";
		$startweek++;
	}
	print "</TABLE>\n";

}
#
#####


##########################################################
# カレンダー本体縦表示
sub html_body_tate
{

#月の第１週めの始めの曜日を求める
$startday = &lib'getyoubi($wyear,$wmon,1);

#第１日
$tama = 1;

#最終日
$tamaend = &lib'getgetumatu($wyear,$wmon);

# 繰返し処理
$yearlydata = "$datadir/yearly_$wyear\.dat";
@yearly = &lib'kurikaeshi_yearlyc3($yearlydata);

# 縦型タイプ

	print "<TABLE BORDER=1 WIDTH=640 cellpadding=3>\n";
	print "<TR BGCOLOR=#CCCC99>";
	print "<TH ALIGN=center nowrap class=\"schedTH\">日</TH>";
	print "<TH ALIGN=center nowrap class=\"schedTH\">曜</TH>";
	if ($USE_ROKUYOU) {print "<TH ALIGN=center nowrap class=\"schedTH\">六曜</TH>";}
	print "<TH ALIGN=center nowrap class=\"schedTH\">時間</TH>";
	print "<TH ALIGN=center WIDTH=$WIDTH2 class=\"schedTH\">スケジュール</TH></TR>";
	while($tama <= $tamaend){
		$i = &lib'getyoubi($wyear,$wmon,$tama);
		($yearly_flag,@yearly_data) = &lib'getyearly("$wmon/$tama",@yearly);
		($monthly_flag,@monthly_data) = &lib'getmonthly($tama,@monthly);
		($weekly_flag,@weekly_data) = &lib'getweekly($i,@weekly);
		$flag = $yearly_flag+$monthly_flag+$weekly_flag;
		&Day;
		&Youbi;

		#六曜
		if ($USE_ROKUYOU) {
			$roku = &qreki'get_rokuyou($wyear,$wmon,$tama);
			print "<TD ALIGN=CENTER class=\"schedT\">$roku_table[$roku]</TD>\n";
		}

		&disp_contents_tate;
		$tama++;
	}
	print "</TABLE>";

}
#
#####


##########################################################
# カレンダーの四角の中のコンテンツ部分　標準タイプ
sub disp_contents
{
	#日付
	$HTMLtd = "<TD valign=\"top\" class=\"schedL\">";
	#今日
	if("$wyear/$wmon/$tama" eq "$year/$mon/$day"){
		$HTMLhi = "<span class=\"$class\" style=\"background-color:$todaycolor\">";
	}else{
		$HTMLhi = "<span class=\"$class\">";
	}
	if ($mgr == 1) {$HTMLhi = "$HTMLhi<A class=\"$class\" HREF=\"$schedulecgi?form=$form&year=$wyear&mon=$wmon&day=$tama\">";}
	$HTMLhi = "$HTMLhi$tama";
	if ($mgr == 1) {$HTMLhi = "$HTMLhi</A>";}
	$HTMLhi = "$HTMLhi<br></span>";

	#六曜
	if ($USE_ROKUYOU) {
		$roku = &qreki'get_rokuyou($wyear,$wmon,$tama);
		$HTMLroku = "<span class=\"rokuyoL\">$roku_table[$roku]<br></span>\n";
	}else{
		$HTMLroku = "";
	}
	#スケジュール
	if(open(DATA,"<$datadir/$wyear.$wmon/$tama.cgi")){
		@datalist = ();
		local($count) = 0;
DATALOAD:
		while(<DATA>){
			chop; push(@datalist, $_);$count++;
		}
		close(DATA);

		@datalist = &lib'sort_data(@datalist);

		$HTMLsch = "<span class=\"schedL\"><b>";
		&make_kurikaeshi_tate_contents;			#祝日表示
		$HTMLsch = "$HTMLsch</b></span>";

		if($#datalist >= 0){
			foreach $eachdata (@datalist){
				($dyear,$dmon,$dday,$dhour,$dmin,$dsec,
				$dhour_s,$dmin_s,$dhour_e,$dmin_e,$dplace,
				$dname,$demail,$dtitle,$dcontent,$drhost,$dpasswd,$dshubetsu,$dpid)
										= split(/\t/,$eachdata);
				$HTMLsch = "$HTMLsch<span class=\"schedL\" style=\"background-color:$shu_color[$dshubetsu]\">";
				#開始時間表示
				if (($dhour_s=="")&&($dmin_s=="")) {
					$HTMLsch = "$HTMLsch<b>$dtitle</b>";
				}else{
					$HTMLsch = "$HTMLsch<b>$dhour_s:$dmin_s $dtitle</b>";
				}
				$HTMLsch = "$HTMLsch<BR></span>";
				$line++;
			}

		#リストサイズが０の時
		}else{
			$HTMLsch = "$HTMLsch<span class=\"schedL\">";
			if($sflag){ $HTMLsch = "$HTMLsch$zen_space<BR>"; }
			$HTMLsch = "$HTMLsch</span>";
		}

	#スケジュールファイルが存在しないとき
	}else{
		$HTMLsch = "<span class=\"schedL\"><b>";
		&make_kurikaeshi_tate_contents;			#祝日表示
		if($sflag){ $HTMLsch = "$HTMLsch$w_jitaim_s$zen_space$w_jitaim_e<BR>"; }
		$HTMLsch = "$HTMLsch</b></span>";
	}

	#HTML書き出し
	print "$HTMLtd$HTMLhi$HTMLroku$HTMLsch</TD>\n";
}
#
#####


##########################################################
# カレンダーの四角の中のコンテンツ部分　年カレンダー
sub disp_contents12
{

	#背景色
	$bg="";

	#スケジュール
	if(open(DATA,"<$datadir/$wyear.$wmon/$tama.cgi")){
		@datalist = ();
		local($count) = 0;
DATALOAD:
		while(<DATA>){
			chop; push(@datalist, $_);$count++;
		}
		close(DATA);

		@datalist = &lib'sort_data(@datalist);

		if($#datalist >= 0){
			foreach $eachdata (@datalist){
				($dyear,$dmon,$dday,$dhour,$dmin,$dsec,
				$dhour_s,$dmin_s,$dhour_e,$dmin_e,$dplace,
				$dname,$demail,$dtitle,$dcontent,$drhost,$dpasswd,$dshubetsu,$dpid)
										= split(/\t/,$eachdata);
				$bg = $shu_color[$dshubetsu];

			}

		}

	}
}
#
#####

##########################################################
# カレンダーの四角の中のコンテンツ部分　縦型タイプ
sub disp_contents_tate
{
	if(open(DATA,"<$datadir/$wyear.$wmon/$tama.cgi")){
		@datalist = ();
		local($count) = 0;
DATALOAD:
		while(<DATA>){
			chop; push(@datalist, $_);$count++;
		}
		close(DATA);
		print "<TD VALIGN=top nowrap class=\"schedT\">";

		@datalist = &lib'sort_data(@datalist);
		&make_kurikaeshi_tate_time;
#時刻表示
		#リストサイズが０でないとき
		if($#datalist >= 0){
			foreach $eachdata (@datalist){
				($dyear,$dmon,$dday,
				$dhour,$dmin,$dsec,
				$dhour_s,$dmin_s,$dhour_e,$dmin_e,$dplace,
				$dname,$demail,$dtitle,$dcontent,$drhost,$dpasswd,$dshubetsu,$dpid)
				= split(/\t/,$eachdata);
				
				if($dhour_s ne "" && $dmin_s ne ""){
					print "$w_jitaim_s$dhour_s:$dmin_s～$w_jitaim_e";
					if($dhour_e ne "" && $dmin_e ne ""){
						print "$w_jitaim_s$dhour_e:$dmin_e$w_jitaim_e";
					}
				}
				print "$w_jitaim_s<BR>$w_jitaim_e\n";
			}
		#リストサイズが０の時
		}else{
			if($sflag){ print "$w_jitaim_s$zen_space$w_jitaim_e<BR>"; }
		}
		print "</TD>";

		$line = 1;
#スケジュール表示
		$HTMLschtd = "<TD valign=\"top\" class=\"schedT\">";
		$HTMLsch="";
		&make_kurikaeshi_tate_contents;
		if($#datalist >= 0){
			foreach $eachdata (@datalist){
				($dyear,$dmon,$dday,$dhour,$dmin,$dsec,
				$dhour_s,$dmin_s,$dhour_e,$dmin_e,$dplace,
				$dname,$demail,$dtitle,$dcontent,$drhost,$dpasswd,$dshubetsu,$dpid)
										= split(/\t/,$eachdata);
				$HTMLsch = "$HTMLsch<span class=\"schedT\">";
				#色あり $HTMLsch = "$HTMLsch<span class=\"schedT\" style=\"background-color:$shu_color[$dshubetsu]\">";
				$HTMLsch = "$HTMLsch$dtitle";
				if($dplace ne ""){
					$HTMLsch = "$HTMLsch / 場所：$dplace";
				}
				#&reply_link;

				#&disp_new;

				$HTMLsch = "$HTMLsch<BR></span>";
				$line++;
			}

		#リストサイズが０の時
		}else{
			$HTMLsch = "$HTMLsch<span class=\"schedT\">";
			if($sflag){ $HTMLsch = "$HTMLsch$zen_space<BR>"; }
			$HTMLsch = "$HTMLsch</span>";
		}

#ファイルが存在しないとき
	}else{
		print "<TD valign=\"top\" class=\"schedT\">";
		&make_kurikaeshi_tate_time;
		if($sflag){ print "$w_jitaim_s$zen_space$w_jitaim_e<BR>"; }
		print "</TD>";
		$HTMLschtd = "<TD WIDTH = $WIDTH2>";
		$HTMLsch = "<span class=\"schedT\">";
		&make_kurikaeshi_tate_contents;
		if($sflag){ $HTMLsch = "$HTMLsch$w_jitaim_s$zen_space$w_jitaim_e<BR>"; }
		$HTMLsch = "$HTMLsch</span>";
	}
	print "$HTMLschtd$HTMLsch</TD>\n";
	print "</TR>";
}
#
#####


##########################################################
# スケジュールの読み込み　ｉｍｏｄｅ
sub disp_contents_i
{
	local($flag);

	$flag = &make_kurikaeshi_tate_contents_i;


	if(open(DATA,"<$datadir/$wyear.$wmon/$tama.cgi")){

		@datalist = ();
		local($count) = 0;
		while(<DATA>){
			chop; push(@datalist, $_);$count++;
		}
		close(DATA);
		@datalist = &lib'sort_data(@datalist);
		$line = 1;

		if($#datalist >= 0){
			foreach $eachdata (@datalist){
				if($line==1){print "<br>\n";}	#予定のある日は最初に改行する
				($dyear,$dmon,$dday,$dhour,$dmin,$dsec,
				$dhour_s,$dmin_s,$dhour_e,$dmin_e,$dplace,
				$dname,$demail,$dtitle,$dcontent,$drhost,$dpasswd,$dshubetsu,$dpid)
										= split(/\t/,$eachdata);
				#開始時間表示
				if (($dhour_s=="")&&($dmin_s=="")) {
					print "&nbsp;$dtitle<br>\n";
				}else{
					print "&nbsp;$dhour_s:$dmin_s&nbsp;$dtitle<br>\n";
				}
				$line++;
			}
		}
	}elsif(!$flag){
		print "<BR>\n";
	}
}


#########
###
sub disp_new
{
#	local($new_time) = &lib'gettimegm($dyear,$dmon,$dday,$dhour,$dmin,$dsec) + ($NEW_TIME * 60 * 60);
#	local($new_time) = timelocal($dsec,$dmin,$dhour,$dday,$dmon-1,$dyear) + ($NEW_TIME * 60 * 60);

	if($customtype[$USE_NEW]){
		local($new_time) = &lib'gettimelocal($dyear,$dmon,$dday,$dhour,$dmin,$dsec) + ($NEW_TIME * 60 * 60);
		local($gt) = time;

		if($new_time > $gt){
			print "<IMG SRC=\"$imagedir/new.gif\" ALT=\"NEW\" BORDER=0>";
		}
	}
}


##########################################################
#縦表示日付
sub Day
{
	#背景色
	$tr_bgcolor = "";

	#もし土曜日ならば
	if($i == 6){
		$tr_bgcolor = "<TR BGCOLOR=\"$satcolor\">";
	#もし日曜日ならば
	}elsif($i == 0){
		$tr_bgcolor = "<TR BGCOLOR=\"$suncolor\">";
	#もし平日ならば
	}else{
		$tr_bgcolor = "<TR BGCOLOR=\"$color\">";
	}
	#もし休日ならば
	if($flag != 0){
		$tr_bgcolor = "<TR BGCOLOR=\"$suncolor\">\n";
	}
	print "$tr_bgcolor";
	#もし今日ならば
	if("$wyear/$wmon/$tama" eq "$year/$mon/$day"){
		print "<TD ALIGN=CENTER class=\"schedTright\" bgcolor=\"$todaycolor\">";
	}else{
		print "<TD ALIGN=CENTER class=\"schedTright\">";
	}
	if ($mgr == 1) {print "<A HREF=\"$schedulecgi?form=$form&year=$wyear&mon=$wmon&day=$tama\">";}
	print "$wmon\/$tama";
	if ($mgr == 1) {print "</A>";}
	print "<BR>";
	print "</TD>\n";
}
#
#####

##########################################################
#
sub Youbi
{
	$weekday = @wdays[$i];

	#平日用style
	$class="norT";
	#もし土曜日ならば
	if($i == 6){
		$class="satT";
	#もし日曜日ならば
	}elsif($i == 0){
		$class="sunT";
	}
	#祝日
	if($flag != 0){
		$class="sunT";
		$weekday="祝";
	}
	#TDタグ書き出し
	print "<TD ALIGN=CENTER class=\"$class\">";
	print "$weekday";
	print "</TD>\n";
}
#
#####


#######################################
# 繰り返しスケジュール　時刻　縦タイプ

sub make_kurikaeshi_tate_time
{
	local($i);

	$sflag = 1;
	if($#yearly_data >= 0){
		for($i = 0;$i <= $#yearly_data;$i++){
			print "$w_jitaim_s$zen_space<BR>$w_jitaim_e";
		}
		$sflag = 0;
	}

}

#######################################
# 繰り返しスケジュール　内容　縦タイプ

sub make_kurikaeshi_tate_contents
{
	local($i);

	$sflag = 1;
	if($#yearly_data >= 0){
		for($i = 0;$i <= $#yearly_data;$i++){
			$HTMLsch = "$HTMLsch$yearly_data[$i]<BR>";
		}
			$sflag = 0;
	}

}


#######################################
# 繰り返しスケジュール　内容　縦タイプ

sub make_kurikaeshi_tate_contents_i
{
	local($i,$flag);
	$flag = 0;

	if($#yearly_data >= 0){
		for($i = 0;$i <= $#yearly_data;$i++){
			$yearly_data[$i] = substr($yearly_data[$i],0,12);
			print "&nbsp;$yearly_data[$i]";
		}
	}

	return($flag);
}

1;
