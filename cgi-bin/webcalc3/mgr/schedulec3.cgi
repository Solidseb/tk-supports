#!/usr/bin/perl
############################################################
#
# ウェッブスケジューラ version 0.30
#
############################################################

# ▼共通
require "webcalconf.cgi"; 
require "lib.pl"; 
require "qreki.pl";

# ▼管理者用
require "mgrconf.cgi"; 

$mgrpfile = "$datadir/mgrp.cgi";
$lockfile = "$datadir/webcal.lock";

# 「種類」の数
if($#shu >= $#shu_color){
	$shu_num = $#shu + 1;
}else{
	$shu_num = $#shu_color + 1;
}

# 入力パラメータ
&lib'getinputfromweb($kanji_code);

# 現在の時刻
($year,$mon,$day,$wday,$hour,$min,$sec) = &lib'getdatetime(time);

# 入力パラメータの加工
$action = $form{'action'};
$fyear = $form{'year'}; $fmon = $form{'mon'}; $fday = $form{'day'};
#入力チェック for Secure version add by mi
if ($fyear =~ /^[0-9]{4}$/){
}else{
	$fyear = $year;
}
if ($fmon =~ /^[0-9]{1,2}$/){
}else{
	$fmon = $mon;
}
if ($fday =~ /^[0-9]{1,2}$/){
}else{
	$fday = $day;
}
$name = $form{'name'}; $email = $form{'email'}; $place = $form{'place'}; $title = $form{'title'};
$content = $form{'content'}; $del_file = $form{'delfile'}; $form = $form{'form'};

$fhour_s = $form{'hour_s'}; $fmin_s = $form{'min_s'};
$fhour_e = $form{'hour_e'}; $fmin_e = $form{'min_e'};

# ユーザエージェント
$agent = $ENV{'HTTP_USER_AGENT'};

# 携帯の判定
if($form eq "i" || $agent =~ "DoCoMo" || $agent =~ "J-PHONE" || $agent =~ "KDDI"){
	$imode = 1;
	$form = "i";
}

# 認証済み？
$auth=0;

# クッキーの取得
&lib'get_cookie($kanji_code);

# HTTPヘッダー
$http_head = "Content-type: text/html\n\n";

##########################################################
#パスワードファイルの作成
if ($form{'req'} eq "new") {
	if (($form{'newmgrp1'} ne "")
	&& ($form{'newmgrp2'} ne "")
	&& ($form{'newmgrp1'} eq $form{'newmgrp2'})) {
		&newMgrpwd;		#パスワードファイルの作成
		&HTMLpassinput;
		exit 0;
	}
#入力パスワードチェック
}elsif($form{'req'} eq "check") {

	&readMgrpwd;			#読み込み
	if ($dmgrp =~ /^\$1\$/) { $salt = 3; } else { $salt = 0; }
	$crypt_passwd = crypt($form{'mgrp'},substr($dmgrp,$salt,2));

	#管理者用パスワードチェック
	if (($dmgrp ne "")
	&& ($crypt_passwd ne "")
	&& ($dmgrp eq $crypt_passwd)){
		#パスワード一致
		&errcnt_zero;
		&lib'set_cookie("cookie_password",$form{'mgrp'},0);
		$auth=1;
	}else{
		#パスワード不一致
		&errcnt_plus;
		&HTMLpassinput;
		exit 0;
	}
#パスワードの変更画面へ
}elsif($form{'req'} eq "modreq") {
	&readMgrpwd;			#読み込み
	&HTMLpassmod;
	exit 0;
#パスワードの変更
}elsif($form{'req'} eq "mod") {

	&readMgrpwd;		#パスワードファイルから読み込み

	if (($form{'oldmgrp'} ne "")
	&& ($form{'newmgrp1'} ne "")
	&& ($form{'newmgrp2'} ne "")
	&& ($form{'newmgrp1'} eq $form{'newmgrp2'})) {

		if ($dmgrp =~ /^\$1\$/) { $salt = 3; } else { $salt = 0; }
		$crypt_passwd = crypt($form{'oldmgrp'},substr($dmgrp,$salt,2));

		#管理者用パスワードチェック
		if (($dmgrp ne "")
		&& ($crypt_passwd ne "")
		&& ($dmgrp eq $crypt_passwd)){
			#パスワード一致
			&modMgrpwd;		#パスワードの変更
			&HTMLpassinput;
			exit 0;
		}else{
			#パスワード不一致
			&errcnt_plus;
			&HTMLpassmod;
			exit 0;
		}
	}else{
			&errcnt_plus;
			&HTMLpassmod;
			exit 0;
	}
}

&readMgrpwd;		#パスワードファイルから読み込み
			#ファイルがなければパスワード設定画面を表示する

##########################################################
# クッキーパスワードチェック
if ($auth ne "1"){
	if ($cookie{'cookie_password'} ne "") {

		if ($dmgrp =~ /^\$1\$/) { $salt = 3; } else { $salt = 0; }
		$crypt_passwd = crypt($cookie{'cookie_password'},substr($dmgrp,$salt,2));

		#管理者用パスワードチェック
		if (($dmgrp ne "")
		&& ($crypt_passwd ne "")
		&& ($dmgrp eq $crypt_passwd)){
			#パスワード一致
			$auth=1;
		}else{
			#パスワード不一致
			&errcnt_plus;
			&HTMLpassinput;
			exit 0;
		}
	}else{
		&HTMLpassinput;		#パスワード入力画面の表示
		exit 0;
	}
}

##########################################################
# 年に一回のスケジュールの読み込み
@yearly = &lib'kurikaeshi_yearly($fyear,$yearlydata,$yearlydata2);
$yearlysize = $#yearly;

@monthly = &lib'kurikaeshi_monthly($monthlydata);
$monthlysize = $#monthly;

@weekly = &lib'kurikaeshi_weekly($weeklydata);
$weeklysize = $#weekly;

##########################################################
# クッキーを使うなら
# 非imode時

if(!$imode){
	if($use_cookie){
		&lib'get_cookie($kanji_code);
		if($form{'name'} ne ""){
			&lib'set_cookie("name",$form{'name'},30);
			&lib'set_cookie("email",$form{'email'},30);
			$cookie_name = $form{'name'};
			$cookie_email = $form{'email'};
		}else{
			$cookie_name = $cookie{'name'};
			$cookie_email = $cookie{'email'};
		}

		@customtype =  split(/\,/,$cookie{'webcal_custom'});
		for($i = 0; $i < $custom_num ;$i++){
			if($customtype[$i] eq ""){
				$customtype[$i] = $use_custom[$i][0];
			}
		}
	}else{
		for($i = 0;$i < $custom_num + 1;$i++){
			$customtype[$i] = $use_custom[$i][0];
		}
	}
}

print "$http_head";

##########################################################
# 特に日付の指定がなければ、今日のスケジュールを表示させる
if($fyear eq ""){
	$fyear = $year; $fmon = $mon; $fday = $day;
}

$datafile = "$datadir/$fyear.$fmon/$fday.cgi";

##########################################################
# もし書き込みのボタンを押されたなら
if($action eq "write" || $action eq "edit_write"){

	#項目入力チェック？
	if($title eq ""){ &lib'error_no_input_form; }

	#新規モード
	if($action eq "write"){
		#ディレクトリ存在チェック
		if(&lib'check_make_dir("$datadir/$fyear.$fmon",$dir_permission)){
			&datawrite;
		#ディレクトリがない場合
		}else{
			#ディレクトリ作成チェック
			if(&lib'check_make_dir("$datadir",$dir_permission)){
				if(lib'check_make_dir("$datadir/$fyear.$fmon",$dir_permission)){
					&datawrite;
				}else{
					&lib'error_cant_make_file;
				}
			#ディレクトリ作成失敗
			}else{
				&lib'error_cant_make_file;
			}
		}
	#編集モード
	}elsif($action eq "edit_write" && $del_file ne ""){
		&edit_write;
	}

##########################################################
# 編集モード

}elsif($action eq "edit"){
	if($del_file ne ""){ &edit_form; }

##########################################################
# 削除モード

}elsif($action eq "delete"){
	if($del_file ne ""){ &datadelete; }
}

# ここからＨＴＭＬ表示部分
############################################################
# ヘッダ
print qq(
<HTML>
<HEAD>
<TITLE>$fyear年$fmon月$fday日のスケジュール</TITLE>
<META HTTP-EQUIV="Cache-Control" CONTENT="no-cache">
</HEAD>
<BODY BGCOLOR="$bgcolor">$tx_jitai_s);

$youbi_tmp = &lib'getyoubi($fyear,$fmon,$fday);
$youbi = @wdays[$youbi_tmp];
$getumatu = &lib'getgetumatu($fyear,$fmon);


# ｉモード新規入力モード
if($action eq "input"){

	#スケジュール登録
	&disp_input_form;

	print "$tx_jitai_e</BODY>\n</HTML>";

	exit 1;

}else{
	# デスクトップブラウザ時
	if(!$imode){
		if($fday == $getumatu){
			if($fmon == 12){
				$preyear = $fyear;
				$nextyear = $fyear + 1;
				$premon = $fmon;
				$nextmon = 1;
				$preday = $fday - 1;
				$nextday = 1;
			}else{
				$preyear = $fyear;
				$nextyear = $fyear;
				$premon = $fmon;
				$nextmon = $fmon+1;
				$preday = $fday - 1;
				$nextday = 1;
			}
		}elsif($fday == 1){
			if($fmon == 1){
				$preyear = $fyear - 1;
				$nextyear = $fyear;
				$premon = 12;
				$nextmon = $fmon;
				$preday = 31;
				$nextday = $fday + 1;
			}else{
				$preyear = $fyear;
				$nextyear = $fyear;
				$premon = $fmon-1;
				$nextmon = $fmon;
				$preday = &lib'getgetumatu($fyear,$fmon-1);
				$nextday = $fday + 1;
			}
		}else{
			$preyear = $fyear;
			$nextyear = $fyear;
			$premon = $fmon;
			$nextmon = $fmon;
			$preday = $fday - 1;
			$nextday = $fday + 1;
		}

		#ヘッダ表示
		&disp_header;

		#繰返しスケジュール
		&repeat_sc;

		#スケジュール表示
		&disp_schedule;

		#スケジュール登録
		&disp_input_form;

	#imodeブラウザ時
	}else{

		#ヘッダ表示
		&disp_header;

		#繰返しスケジュール
		&repeat_sc;

		#スケジュール表示
		&disp_schedule;
	}

	print "$tx_jitai_e</BODY>\n</HTML>";
}


exit 0;

######################################################
# ヘッダ表示
#
sub disp_header
{
	if($imode){ # imode時
		print "<CENTER>$fyear/$fmon/$fday($youbi)</CENTER>";
		print "<CENTER>";
		print "<A HREF = \"$schedulecgi?year=$fyear&mon=$fmon&day=$fday&action=input\" accesskey=\"1\">&#63879;Schedule 登 録</A><BR>";
		print "<A HREF = \"$webcalcgi?year=$fyear&mon=$fmon\" accesskey=\"2\">&#63880;Calendarへ戻る</A>";
		print "</CENTER><HR>";
	}else{

		print "<TABLE BORDER=0 CELLPADDING=4 WIDTH=100%><TR><TD BGCOLOR=#FF2D15>\n";
		print "<CENTER><B><FONT SIZE=\"+2\" COLOR=\"#FFFFFE\">$fyear年$fmon月$fday日（$youbi曜日) 　\n";

		print "</FONT></B></CENTER></TD></TR></TABLE>\n";
		print "<CENTER>";

		if(@nen[0] > $preyear && $premon == 12 && $preday == 31){
			print "←前の日・";
		}else{
			print "←<A HREF = \"$schedulecgi?form=$form&year=$preyear&mon=$premon&day=$preday\">前の日</A>・";
		}
		if(@nen[$nensize] < $nextyear && $nextmon == 1 && $nextday == 1){
			print "次の日→／\n";
		}else{
			print "<A HREF = \"$schedulecgi?form=$form&year=$nextyear&mon=$nextmon&day=$nextday\">次の日</A>→／\n"
		}
		if("$fyear/$fmon/$fday" ne "$year/$mon/$day"){
			print "<A HREF = \"$schedulecgi?form=$form\">今日のスケジュール</A>／\n";
		}else{
			print "今日のスケジュール／\n";
		}
		print "<A HREF = \"#touroku\">スケジュール登録</A>／";
		print "<A HREF = \"$webcalcgi?form=$form&year=$fyear&mon=$fmon\">カレンダーへ戻る</A>\n";

		print "<TABLE BORDER=0 CELLPADDING=4 WIDTH=100%><TR><TD BGCOLOR=#FF750F>\n";
		print "<CENTER>$s_jitai_s登録済スケジュール$s_jitai_e</CENTER>\n";
		print "</TD></TR></TABLE><P>\n";
	}

}
######################################################
# スケジュール表示
#
sub disp_schedule
{
	local($eachdata);

	$page = $form{'page'};
	$max_sc = 3;

	@datalist = ();

	if(open(DATA,"<$datafile")){
		while (<DATA>) {chop; push(@datalist, $_);}
		close(DATA);

		@datalist = &lib'sort_data(@datalist);
		$dallinenum = 1;

		if(!$imode){
			foreach $eachdata (@datalist){
				&read_schedule($eachdata);
			}
		}else{
			for($scn = $page*$max_sc ;$scn < $page*$max_sc + $max_sc ; $scn++){
				if($scn > $#datalist) { last; }
				$eachdata = $datalist[$scn];
				&read_schedule($eachdata);

			}
			$next_page = $page + 1;
			$pre_page = $page -1;

			if($page != 0){ print "<A HREF = \"$schedulecgi?page=$pre_page&year=$fyear&mon=$fmon&day=$fday\">前ページ</A><BR>"; }

			if($scn < $#datalist+1) { print "<A HREF = \"$schedulecgi?page=$next_page&year=$fyear&mon=$fmon&day=$fday\">次ページ</A><BR>"; }

		}
	}else{
		print "現在スケジュールはありません。<BR><HR>\n";
	}

}

sub read_schedule
{
	local($eachdata) = @_;

			($dyear,$dmon,$dday,$dhour,$dmin,$dsec,$dhour_s,$dmin_s,$dhour_e,$dmin_e,$dplace,
			$dname,$demail,$dtitle,$dcontent,$drhost,$dpasswd,$dshubetsu,$dpid,$sendmail,$use_hen,$dwrite_tsuchi)
										 = split(/\t/,$eachdata);

			if($dshubetsu != 0){
				print "<div align=\"left\"><SPAN STYLE=\"background-color:$shu_color[$dshubetsu]\"><B>[@shu[$dshubetsu]]$dtitle</B></SPAN>　";
			} else {
				print "<div align=\"left\"><B>$dtitle</B><BR>";
			}

			if($dhour_s ne "" && $dmin_s ne ""){
				if(!$imode){
					print "<B>　時間： $dhour_s時 $dmin_s分 ～ </B>";
				}else{
					print "<B>$dhour_s:$dmin_s ～ </B>";
				}
				if($dhour_e ne "" && $dmin_e ne ""){
					if(!$imode){
						print "<B>$dhour_e時 $dmin_e分　</B>";
					}else{
						print "<B>$dhour_e:$dmin_e<BR></B>";
					}
				}
			}

			if($dplace ne "" ){
				if(!$imode){
					print "<B>　場所：$dplace</B>";
				}else{
					print "<B>$dplace</B>";
				}
			}

			if(!$imode){ $dcontent = &lib'inline_link($dcontent); }

			if(!$imode){
				print "<P>\n<BLOCKQUOTE>$dcontent</BLOCKQUOTE><P>\n";
			}else{
				print "<P>$dcontent<P>\n";
			}

			print "</div>";

			$del_file = $dmon . $dday . $dhour . $dmin . $dsec . $dpid;

			print "<FORM action = $schedulecgi METHOD=POST>\n";
			print "<INPUT TYPE=hidden NAME=form VALUE=$form>\n";
			print "<INPUT TYPE=hidden NAME=delfile VALUE=$del_file>\n";
			print "<INPUT TYPE=hidden NAME=year VALUE=$fyear>\n";
			print "<INPUT TYPE=hidden NAME=mon VALUE=$fmon>\n";
			print "<INPUT TYPE=hidden NAME=day VALUE=$fday>\n";

			print "<DIV ALIGN=left>";
			print "書いた日時：$dyear年 $dmon月 $dday日 $dhour時 $dmin分 $dsec秒<BR>\n";

#			print "パスワード：<INPUT TYPE=password NAME=passwd SIZE=20>\n";
			print "<INPUT TYPE=\"radio\" NAME=\"action\" VALUE=\"delete\">削除　";
			print "<INPUT TYPE=\"radio\" NAME=\"action\" VALUE=\"edit\">修正　";

			print "<INPUT TYPE=submit VALUE=\"実　行\">\n";
			print "</FORM>\n<FONT>\n";

			print "$tx_jitai_e";
			print "</DIV>";

			print "<HR>\n";
			$dallinenum++;

}

######################################################
#　スケジュール新規書き込み
#
sub datawrite
{
	local($write_tsuchi) = 0;
	local($i,$j);

	$crypt = &lib'MakeCrypt($form{'passwd'});
	if($crypt eq ''){
		print "<H2>$crypt:パスワードの暗号化に失敗しました。戻って再度実行してください。</H2>";
		exit 1;
	}

	for($i = 0;$i < $mail_group_num+1;$i++){
		$write_tsuchi += $form{$i};
	}

	if(&lib'flock_on($lockfile) == 0){
		if(open(DATA,">>$datafile")){
			$datalist = join("\t",$year,
						$mon,
						$day,
						$hour,
						$min,
						$sec,
						$fhour_s,
						$fmin_s,
						$fhour_e,
						$fmin_e,
						$form{'place'},
						$form{'name'},
						$form{'email'},
						$form{'title'},
						$form{'content'},
						$ENV{'REMOTE_HOST'},
						$crypt,
						$form{'shubetsu'},
						$$,
						$form{'sendmail'},
						$form{'use_hen'},
						$write_tsuchi
			);
			print DATA "$datalist\n";
			close(DATA);
			chmod $file_permission, "$datafile";
			&lib'flock_off($lockfile);

			# 管理者通知
			if($admin_send){ &sendmail('書込',$admin_email,$fyear,$fmon,$fday,$fhour_s,$fmin_s,$fhour_e,$fmin_e,$place,$name,$email,$title,$content); }	#管理者に内容通知

			# ユーザー通知
			if($use_write_tsuchi && $write_tsuchi){
				for($j = 0;$j < $mail_group_num+1 + 1;$j++){
					if($form{$j} != 0){
						for($i = 1;$i <= $#{$mail_group[$j]};$i++){
							&sendmail('書込',$mail_group[$j][$i],$fyear,$fmon,$fday,$fhour_s,$fmin_s,$fhour_e,$fmin_e,$place,$name,$email,$title,$content);
						}
					}
				}
			}

		}else{
			&lib'flock_off($lockfile);
			&lib'error_cant_make_file;
		}
	}else{
		&lib'error_file_locking;
	}
}

######################################################
#　スケジュール削除
#
sub datadelete
{

	if(open(DATA,"<$datafile")){
		
		$delline = &check_file_line;
		close(DATA);

		if ($dpasswd =~ /^\$1\$/) { $salt = 3; } else { $salt = 0; }
		$crypt_passwd = crypt($form{'passwd'},substr($dpasswd,$salt,2));

		if($delline != 0 && ($dpasswd eq $crypt_passwd || $delpasswd eq $form{'passwd'})){

			&datadelete1;
			unlink("$datafile");
			if(-z "$datafile.tmp"){
				unlink("$datafile.tmp");
			}else{
				rename("$datafile.tmp","$datafile");
			}

			$reply = $fday . "_" . $dmon . $dday . $dhour . $dmin . $dsec . $dpid;
			$replyfile = "$datadir/$fyear.$fmon/reply/$reply";
			if(-r "$replyfile"){
				unlink("$replyfile");
			}
		}else{
			&lib'error_illeagal_passwd;
		}
	}
}

sub datadelete1
{
	local($t1,$t2,$t3,$t4,$t5,$t6,$j);
	local($tyear,$tmon,$tday,$thour_s,$tmin_s,$thour_e,$tmin_e,$tplace,$tname,$temail,$ttitle,$tcontent,$trhost,$tpasswd,$tshubetsu,$tpid,$sendmail,$use_hen,$twrite_tsuchi);
	local($mask) = 1;

	if(&lib'flock_on($lockfile) == 0){
		local($count) = 0;
		@datalist = ();
		if(open(DATA,"<$datafile")){
			if(open(NEWDATA,">$datafile.tmp")){
				eval {flock( DATA, 2);};
				while (<DATA>){
					$count++;
					#削除時
					if($count != $delline){
						print NEWDATA $_;
					}else{
						($t1,$t2,$t3,$t4,$t5,$t6,$thour_s,$tmin_s,$thour_e,$tmin_e,$tplace,$tname,$temail,
							$ttitle,$tcontent,$trhost,$tpasswd,$tshubetsu,$tpid,$sendmail,$use_hen,$twrite_tsuchi) = split(/\t/,$_);
					}
				}
				close(NEWDATA);
				chmod $file_permission,"$datafile.tmp";
			}else{
				close(DATA);
				&lib'flock_off($lockfile);
				&lib'error_cant_make_file;
			}
			close(DATA);
		}
		&lib'flock_off($lockfile);
		if($admin_send){ &sendmail('削除',$admin_email,$fyear,$fmon,$fday,$thour_s,$tmin_s,$thour_e,$tmin_e,$tplace,$tname,$temail,$ttitle,$tcontent); }	#管理者に内容通知

		#ユーザー通知
		if($use_write_tsuchi && $twrite_tsuchi){
			for($j = 0;$j < $mail_group_num + 1 ;$j++){
				if($twrite_tsuchi & $mask){
					for($i = 1;$i <= $#{$mail_group[$j]};$i++){
						&sendmail('削除',$mail_group[$j][$i],$fyear,$fmon,$fday,$fhour_s,$fmin_s,$fhour_e,$fmin_e,$tplace,$tname,$temail,$ttitle,$tcontent);
					}
				}
				$mask = $mask << 1;
			}
		}

	}else{
		&lib'error_file_locking;
	}
}

######################################################
#　スケジュール修正
#
sub edit_write
{
	if(open(DATA,"<$datafile")){
		$delline = &check_file_line;
		close(DATA);

		if($delline != 0){
			&edit_write1;
			unlink("$datafile");
			rename("$datafile.tmp","$datafile");
		}
	}
}

sub edit_write1
{
	local($write_tsuchi) = 0;
	local($i,$j);


	if ($dpasswd =~ /^\$1\$/) { $salt = 3; } else { $salt = 0; }
	$crypt_passwd = crypt($form{'passwd'},substr($dpasswd,$salt,2));

	#パスワード、管理者用パスワードチェック
	if($dpasswd ne $crypt_passwd && $delpasswd ne $form{'passwd'}){
		&lib'error_illeagal_passwd;
	}


	for($i = 0;$i < $mail_group_num+1;$i++){
		$write_tsuchi += $form{$i};
	}

	if(&lib'flock_on($lockfile) == 0){
		local($count) = 0;
		if(open(DATA,"<$datafile")){
			if(open(NEWDATA,">$datafile.tmp")){
				eval {flock( DATA, 2);};
				while (<DATA>) {
					$count++;
					if($count != $delline){
						print NEWDATA $_;
					}else{

						$editlist = join("\t",$dyear,
							$dmon,
							$dday,
							$dhour,
							$dmin,
							$dsec,
							$fhour_s,
							$fmin_s,
							$fhour_e,
							$fmin_e,
							$form{'place'},
							$form{'name'},
							$form{'email'},
							$form{'title'},
							$form{'content'},
							$drhost,
							$dpasswd,
							$form{'shubetsu'},
							$dpid,
							$form{'sendmail'},
							$form{'use_hen'},
							$form{'write_tsuchi'}
						);
						print NEWDATA "$editlist\n";
						if($admin_send){ &sendmail("修正",$admin_email,$fyear,$fmon,$fday,$fhour_s,$fmin_s,$fhour_e,$fmin_e,$place,$name,$email,$title,$content); }	#管理者に内容通知

						# ユーザー通知
						if($use_write_tsuchi && $write_tsuchi){
							for($j = 0;$j < $mail_group_num+1 + 1;$j++){
								if($form{$j} != 0){
									for($i = 1;$i <= $#{$mail_group[$j]};$i++){
										&sendmail('修正',$mail_group[$j][$i],$fyear,$fmon,$fday,$fhour_s,$fmin_s,$fhour_e,$fmin_e,$place,$name,$email,$title,$content);
									}
								}
							}
						}
					}
				}
				close(NEWDATA);
				chmod $file_permission,"$datafile.tmp";

			}else{
				close(DATA);
				&lib'flock_off($lockfile);
				&lib'error_cant_make_file;
			}
			close(DATA);
		}
		&lib'flock_off($lockfile);
	}else{
		&lib'error_file_locking;
	}
}
########################################################
# スケジュール新規入力時のフォーム表示
#
sub disp_input_form
{
#スケジュール入力フォーム表示


	print "<A NAME=\"touroku\"></A>";

	if($imode){ print "$s_jitai_sスケジュール登録$s_jitai_e\n"; }

	$dname = $cookie_name; $demail = $cookie_email; $dhour_s = ""; $dmin_s = ""; $dhour_e = ""; $dmin_e = "";
	$dshubetsu = $shu - 1; $dtitle = ""; $dplace = ""; $dcontent = ""; $sendmail = 0; $use_hen = 0; $dwrite_tsuchi = 0;

	if(!$imode){
		&disp_normal_form("write");
	}else{
		&disp_imode_form("write");
	}

}

#########################################################
# スケジュール編集
#
sub edit_form
{
	$delline = 0;
	@datalist = ();
	if(open(DATA,"<$datafile")){
		$delline = &check_file_line;
		close(DATA);
	}

	if ($dpasswd =~ /^\$1\$/) { $salt = 3; } else { $salt = 0; }
	$crypt_passwd = crypt($form{'passwd'},substr($dpasswd,$salt,2));

	#パスワード、管理者用パスワードチェック
	if($dpasswd eq $crypt_passwd || $delpasswd eq $form{'passwd'}){
		&disp_edit_form;
		exit 0;
	}else{
		&lib'error_illeagal_passwd;
	}

	exit 0;
}

#########################################################
#　スケジュール修正時の入力フォーム表示
#
sub disp_edit_form
{

	$youbi_tmp = &lib'getyoubi($fyear,$fmon,$fday);
	$youbi = @wdays[$youbi_tmp];

	print qq(
	<HTML>
	<HEAD>
	<TITLE>$fyear年$fmon月$fday日のスケジュール</TITLE>
	<META HTTP-EQUIV="Cache-Control" CONTENT="no-cache">
	</HEAD>
	<BODY BGCOLOR="$bgcolor">
	);

	
	if(!$imode){
		print "<TABLE BORDER=0 CELLPADDING=4 WIDTH=100%><TR><TD BGCOLOR=#FF2D15>\n";
		print "<CENTER><B><FONT SIZE=\"+2\" COLOR=\"#FFFFFE\">";
		print "$fyear年$fmon月$fday日（$youbi曜日）のスケジュール修正";
		print "</FONT></B></CENTER></TD></TR></TABLE>\n";
	}else{
		print "<center>スケジュール修正</center><HR>\n";

	}

	local($time,$stime);

	if(!$imode){
		&disp_normal_form("edit_write");
	}else{
		&disp_imode_form("edit_write");
	}

}


# フォーム表示－名前
sub disp_name
{
	local($imode) = @_;
	if($imode){ $size = 15; } else { $size = 20; }
	print "<INPUT TYPE=text NAME=name VALUE=\"$dname\" SIZE=\"$size\">";

}

# フォーム表示－電子メール
sub disp_email
{
	local($imode) = @_;
	if(!$imode){ $size = 30; } else { $size = 15; }
	print "<INPUT TYPE=text NAME=email VALUE=\"$demail\" SIZE=\"$size\">";
}

# フォーム表示－開始時
sub disp_hour_s
{
	$time = 0;
	print "<SELECT NAME=\"hour_s\">\n";
	if($dhour_s eq ""){
		print "<OPTION VALUE=\"\" SELECTED>未選択\n";
	}else{
		print "<OPTION VALUE=\"\">未選択\n";
	}
	while($time <= 25){
		$stime = sprintf("%02d", $time);
		if($dhour_s eq $stime || $dhour_s eq $time){
			print "<OPTION VALUE=$stime SELECTED>$time\n";
		}else{
			print "<OPTION VALUE=$stime>$time\n";
		}
		$time++;
	}
	print "</SELECT> 時　\n";
}

# フォーム表示－開始分
sub disp_min_s
{
	$time = 0;
	print "<SELECT NAME=\"min_s\">\n";
	if($dmin_s eq ""){
		print "<OPTION VALUE=\"\" SELECTED>未選択\n";
	}else{
		print "<OPTION VALUE=\"\">未選択\n";
	}
	while($time <= 50){
		$stime = sprintf("%02d", $time);
		if($dmin_s eq $stime){
			print "<OPTION VALUE=$stime SELECTED>$stime\n";
		}else{
			print "<OPTION VALUE=$stime>$stime\n";
		}
		$time += 10;
	}
	print "</SELECT> 分　～　\n";
}
# フォーム表示－終了時
sub disp_hour_e
{
	$time = 0;
	print "<SELECT NAME=\"hour_e\">\n";
	if($dhour_e eq ""){
		print "<OPTION VALUE=\"\" SELECTED>未選択\n";
	}else{
		print "<OPTION VALUE=\"\">未選択\n";
	}
	while($time <= 25){
		$stime = sprintf("%02d", $time);
		if($dhour_e eq $stime || $dhour_e eq $time){
			print "<OPTION VALUE=$stime SELECTED>$time\n";
		}else{
			print "<OPTION VALUE=$stime>$time\n";
		}
		$time++;
	}
	print "</SELECT> 時　\n";
}
# フォーム表示－終了分
sub disp_min_e
{
	$time = 0;
	print "<SELECT NAME=\"min_e\">\n";
	if($dmin_e eq ""){
		print "<OPTION VALUE=\"\" SELECTED>未選択\n";
	}else{
		print "<OPTION VALUE=\"\">未選択\n";
	}
	while($time <= 50){
		$stime = sprintf("%02d", $time);
		if($dmin_e eq $stime){
			print "<OPTION VALUE=$stime SELECTED>$stime\n";
		}else{
			print "<OPTION VALUE=$stime>$stime\n";
		}
		$time += 10;
	}
	print "</SELECT> 分\n";
}

# フォーム表示－種別
sub disp_shu
{
	#種別数が１の場合は種別選択のフォーム表示をしない
	if($shu_num > 1){
		$i = $shu_num-1;
		print "<SELECT NAME=\"shubetsu\">\n";
		while($i > 0){
			if($i eq $dshubetsu){
				print "<OPTION VALUE=$i SELECTED>$shu[$i]\n";
			}else{
				print "<OPTION VALUE=$i>$shu[$i]\n";
			}
			$i--;
		}
		print "</SELECT>\n";
	}
}

# フォーム表示－タイトル
sub disp_title
{
	local($imode) = @_;
	if($imode){ $size = 15; } else { $size = 65; }
	print "<INPUT TYPE=text NAME=title VALUE=\"$dtitle\" SIZE=\"$size\">\n";
}

# フォーム表示－場所
sub disp_place
{
	local($imode) = @_;
	if($imode){ $size = 15; } else { $size = 65; }
	print "<INPUT TYPE=text NAME=place VALUE=\"$dplace\" SIZE=\"$size\">\n";
}

# フォーム表示－内容
sub disp_contents
{
	local($imode) = @_;
	if($imode){ $size = 15; } else { $size = 65; }
	$dcontent =~ s/<BR>/\n/g;
	print "<TEXTAREA NAME=content ROWS=7 COLS=\"$size\" WRAP=virtual>$dcontent</TEXTAREA>\n";

}
# フォーム表示－パスワード
sub disp_passwd
{
	local($imode) = @_;
	if($imode){ $size = 15; } else { $size = 20; }
	print "<INPUT TYPE=password NAME=passwd SIZE=\"$size\">　\n";
}

# フォーム表示－ボタン
sub disp_button
{
	print "<INPUT TYPE=submit VALUE=\"書　込\"><INPUT TYPE=reset VALUE=\"クリア\"></P><HR>";
}

#########################################################
# 通常ブラウザでのフォーム表示
# 
#
sub disp_normal_form
{
	local($w_mode) = @_;

	print "<FORM action = $schedulecgi METHOD=POST>\n";
	print "<INPUT TYPE=hidden NAME=form VALUE=\"$form\">\n";
	print "<INPUT TYPE=hidden NAME=year VALUE=\"$fyear\">\n";
	print "<INPUT TYPE=hidden NAME=mon VALUE=\"$fmon\">\n";
	print "<INPUT TYPE=hidden NAME=day VALUE=\"$fday\">\n";
	print "<INPUT TYPE=hidden NAME=delfile VALUE=\"$del_file\">\n";
	print "<INPUT TYPE=hidden NAME=action VALUE=\"$w_mode\">\n";

	print "<TABLE BORDER=\"0\" CELLSPACING=\"1\" CELLPADDING=\"8\" WIDTH=\"100%\">\n";

	if(!$imode){
		print "<TH BGCOLOR=#804000 COLSPAN=\"2\" ><FONT SIZE=\"+1\" COLOR=\"#FFFFFE\">スケジュール登録</FONT></TH>\n";
	}

	print "<TR BGCOLOR=\"#FEE09C\"><TH NOWRAP>種　　別</TH><TD>";
	&disp_shu;
	print "</TD></TR>\n";

	print "<TR BGCOLOR=\"#FEE09C\"><TH NOWRAP>タイトル</TH><TD>";
	&disp_title($imode);
	print "</TD></TR>\n";

	print "<TR BGCOLOR=\"#FEE09C\"><TH NOWRAP>時　　間</TH><TD>";
	&disp_hour_s;
	&disp_min_s;
	&disp_hour_e;
	&disp_min_e;
	print "</TD></TR>\n";

	print "<TR BGCOLOR=\"#FEE09C\"><TH NOWRAP>場　　所</TH><TD>";
	&disp_place($imode);
	print "</TD></TR>\n";

#	print "<TR BGCOLOR=\"#FEE09C\"><TH NOWRAP>パスワード</TH><TD>";
#	&disp_passwd($imode);
#	print "</TD></TR>\n";

	print "</TABLE>\n";
	&disp_button;

	print "</FORM>\n";
}


sub check_file_line
{
	local($delline) = 0;

	while (<DATA>) {
		chop;
		($dyear,$dmon,$dday,$dhour,$dmin,$dsec,$dhour_s,$dmin_s,$dhour_e,$dmin_e,$dplace,
		$dname,$demail,$dtitle,$dcontent,$drhost,$dpasswd,$dshubetsu,$dpid,$sendmail,$use_hen,$dwrite_tsuchi) = split(/\t/,$_);
		$dfile = $dmon . $dday . $dhour . $dmin . $dsec . $dpid;
		$delline++;
		if($dfile eq $del_file){ 
			return $delline;
		}
	}
	return 0;
}

######################################################
#　時が定義され、分が未定義の時は分を"00"とする
#
#　引数：時、分
#　戻値：分
#

sub check_time
{
	local($hour_s,$min_s,$hour_e,$min_e) = @_;

	if($hour_s ne "" && $hour_e ne ""){
		if($hour_s > $hour_e){return (0); }
		if($hour_s == $hour_e && $min_s > $min_e){return(0); }
	}
	
	return(1);

}

sub repeat_sc
{
	local($i);

	($yearly_flag,@yearly_data) = &lib'getyearly("$fmon/$fday",@yearly);

	$flag = $yearly_flag;
	print "<div align=\"left\"><B>";

	if($#yearly_data >= 0){
		for($i = 0;$i <= $#yearly_data;$i++){
			print "$yearly_data[$i]<BR>";
		}
		print "<HR>\n";
	}

	print "</B></div>";
}



############################################################
# パスワード入力画面表示
sub HTMLpassinput
{
print "$http_head";
print qq(
<HTML>
<HEAD>
<TITLE>パスワード入力</TITLE>
<META HTTP-EQUIV="Cache-Control" CONTENT="no-cache">
</HEAD>
<BODY BGCOLOR="#a6b3ff"><!--青-->
<div align="center">
<H1>パスワードを入力してください</H1>
<form action="$schedulecgi" method="post">
<table border="1" width="400" height="100"><tr><td align="center" valign="middle">
パスワード：　<input name="mgrp" type="password">
<input type="submit" value="送信">
<input type="hidden" name="req" value="check">
<input type="hidden" name="year" value="$fyear">
<input type="hidden" name="mon" value="$fmon">
<input type="hidden" name="day" value="$fday">
</td></tr></table>
</form>
<a href="$schedulecgi?req=modreq&year=$fyear&mon=$fmon&day=$fday">パスワードの変更</a><br>
<font size=-1>パスワードエラーは$errcnt回です<br>
最後のエラーはIPアドレス[$errip]からのアクセスでした</font><br>
</div>
</body></html>
);
}

############################################################
# パスワード新規作成画面表示
sub HTMLpassnew
{
print "$http_head";
print qq(
<HTML>
<HEAD>
<TITLE>パスワード作成</TITLE>
<META HTTP-EQUIV="Cache-Control" CONTENT="no-cache">
</HEAD>
<BODY BGCOLOR="#e6cdd8">
<div align="center">
<H1>パスワード作成</H1>
<form action="$schedulecgi" method="post">
<table border="1"><tr><td>
<table border="0" cellpadding="3" width="400" height="100">
<tr>
<td align="right">新しいパスワード：</td><td align="left"><input name="newmgrp1" type="password"></td>
</tr>
<tr>
<td align="right">新しいパスワード確認：</font></td><td align="left"><input name="newmgrp2" type="password"></td>
</tr>
<tr>
<td colspan="2" align="center">
<input type="submit" value="　　　送　信　　　">
<input type="hidden" name="req" value="new">
<input type="hidden" name="year" value="$fyear">
<input type="hidden" name="mon" value="$fmon">
<input type="hidden" name="day" value="$fday">
</td>
</tr></table>
</td></tr></table>
</form>
</div>
</body></html>
);
}

############################################################
# パスワード変更画面表示
sub HTMLpassmod
{
print "$http_head";
print qq(
<HTML>
<HEAD>
<TITLE>パスワード変更</TITLE>
<META HTTP-EQUIV="Cache-Control" CONTENT="no-cache">
</HEAD>
<BODY BGCOLOR="$body_bgcolor">
<div align="center">
<H1>パスワード変更</H1>
<form action="$schedulecgi" method="post">
<table border="1"><tr><td>
<table border="0" cellpadding="3" width="400" height="100">
<tr>
<td align="right">パスワード：</td><td align="left"><input name="oldmgrp" type="password"></td>
</tr>
<tr>
<td align="right">新しいパスワード：</td><td align="left"><input name="newmgrp1" type="password"></td>
</tr>
<tr>
<td align="right">新しいパスワード確認：</td><td align="left"><input name="newmgrp2" type="password"></td>
</tr>
<tr>
<td colspan="2" align="center">
<input type="submit" value="　　　送　信　　　">
<input type="hidden" name="req" value="mod">
<input type="hidden" name="year" value="$fyear">
<input type="hidden" name="mon" value="$fmon">
<input type="hidden" name="day" value="$fday">
</td>
</tr></table>
</td></tr></table>
</form>
<font size=-1>パスワードエラーは$errcnt回です<br>
最後のエラーはIPアドレス[$errip]からのアクセスでした</font><br>
</div>
</body></html>
);
}

############################################################
# 管理者パスワードの新規作成
sub newMgrpwd
{
	$newmgrp = &lib'MakeCrypt($form{'newmgrp1'});	# 新しいパスワード

	if(&lib'flock_on($lockfile) == 0){
		if(open(DATA,"<$mgrpfile")){
			&lib'flock_off($lockfile);
			&lib'error_file_mgrp;	#パスワードファイル作成エラー
		}else{
			# パスワードファイルの作成
			if(open(DATA,">$mgrpfile")){
				$errcnt = 0;
				$datalist = join("\t",$errcnt,$newmgrp,$errip);
				print DATA "$datalist\n";
				close(DATA);
#				chmod $file_permission, "$mgrpfile";
				&lib'flock_off($lockfile);
			}
		}
	}else{
		&lib'error_file_locking;
	}
}


############################################################
# 管理者パスワードの書き込み
sub modMgrpwd
{
	$newmgrp = &lib'MakeCrypt($form{'newmgrp1'});	# 新しいパスワード

	if(&lib'flock_on($lockfile) == 0){
		# パスワードファイルのオープン
		if(open(DATA,">$mgrpfile")){
			# パスワードの変更
			$datalist = join("\t",$errcnt,$newmgrp,$errip);
			print DATA "$datalist\n";
			close(DATA);
			chmod $file_permission, "$mgrpfile";
			&lib'flock_off($lockfile);
		}else{
			&lib'flock_off($lockfile);
			&lib'error_cant_make_file;
		}
	}else{
		&lib'error_file_locking;
	}
}


############################################################
# 管理者パスワードデータ読み込み
sub readMgrpwd
{
	if(open(DATA,"<$mgrpfile")){
		while (<DATA>) {chop; push(@datalist, $_);}
		close(DATA);

		foreach $eachdata (@datalist){
			($errcnt,$dmgrp,$errip) = split(/\t/,$eachdata);
		}
	}else{
		&HTMLpassnew;
		exit 0;
	}
}

############################################################
# パスワードエラー加算
sub errcnt_plus
{
	if(&lib'flock_on($lockfile) == 0){
		if(open(DATA,">$mgrpfile")){
			#エラーカウントアップ
			$errcnt += 1;
			#IPアドレス
			$errip = $ENV{'REMOTE_ADDR'};
			#書き出し
			$datalist = join("\t",$errcnt,$dmgrp,$errip);
			print DATA "$datalist\n";
			close(DATA);
		}

		&lib'flock_off($lockfile);

	}else{
		&lib'error_file_locking;
	}
}

############################################################
# パスワードエラーゼロクリア
sub errcnt_zero
{
	if(&lib'flock_on($lockfile) == 0){
		if(open(DATA,">$mgrpfile")){
			#エラーカウント０
			$errcnt = 0;
			#書き出し
			$datalist = join("\t",$errcnt,$dmgrp,$errip);
			print DATA "$datalist\n";
			close(DATA);
		}

		&lib'flock_off($lockfile);

	}else{
		&lib'error_file_locking;
	}
}
