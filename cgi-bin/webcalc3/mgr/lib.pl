package lib;
############################################################
# ウェッブカレンダ＆スケジューラ用ライブラリ
# 
# Ver 0.21b Time::Localモジュールを使用しないようにした。
# 
# ----------------------------------------------------------
# オリジナル情報
# 制作者： Koji Onishi
# 制作日： 98.10.15
# 種類： フリーウエア
# 動作確認： FreeBSD & perl5
# 
############################################################
require "jcode.pl";

############################################################
# 月末の数字
@monthday = ('31','28','31','30','31','30','31','31','30','31','30','31');

###########################################################
#　返信があるかないかをチェックする
#　引数：ファイルパス
#　戻値：1=存在する
#　　　　0=存在しない、またはサイズが０である
sub check_henshin
{
	local($file) = @_;
	if(-r "$file"){
		if(-z "$file"){
			return 0;
		}
		return 1;
	}else{
		return 0
	}

}

############################################################
# ディレクトリがあるかないかをチェックし、
# なければ書込みモードでディレクトリを作成する
# 引き数：ディレクトリパス
# 戻り値：1=ディレクトリが存在する、もしくはディレクトリが作成された
# 　　　　0=ディレクトリを作成できない
#
sub check_make_dir
{
	local($dir,$dir_pms) = @_;
	if(-d "$dir"){
		return 1;
	}else{
		if(mkdir("$dir",0777)){
			chmod $dir_pms, "$dir";
			system "touch $dir/index.html";
			return 1;
		}else{
			return 0;
		}
	}
}

############################################################
# Windows対応flock
# 引き数：ロックファイル名
# 戻り値：1=ロックファイルが存在する
# 　　　　0=ロックファイルが存在しない
#
sub flock_on
{
	local($lockfile) = @_;
	if(-f "$lockfile"){
		return 1;
	}else{
		if(open(LOCK,">$lockfile")){
			print LOCK "lock";
			close(LOCK);
			chmod $file_permission, "$lockfile";
			return 0;
		}else{
			&error_make_lockfile;
			return 0;
		}
	}
}

############################################################
# Windows対応unflock
# 引き数：ロックファイル名
# 戻り値：なし
#
sub flock_off
{
	local($lockfile) = @_;
	if(-f "$lockfile"){
		unlink("$lockfile");
	}
}

############################################################
# 月末の数字を求める
# 引き数：年、月
# 戻り値：月末の数字
#
sub getgetumatu
{	
	local($year,$mon) = @_;
	if($mon != 2){
		return(@monthday[$mon-1]);
	}else{
		if(&leapyear($year)){
			return(29);
		}else{
			return(28);
		}
	}
}

############################################################
# 曜日を求める
# 引き数：年、月、日
# 戻り値：曜日の数字
# 0="日",1="月",2="火",3="水",4="木",5="金",6="土"
#
sub getyoubi
{
	local($year,$mon,$day) = @_;

	$time = &gettime($year,$mon,$day);

	($sec,$min,$hour,$day,$mon,$year,$wday,$yday,$isdst) = gmtime($time);
	return($wday);
}

############################################################
# localtimeやgmtimeの引き数にできる数字を求める
# 引き数：年、月、日
# 戻り値：localtimeやgmtimeの引き数にできる数字
#
sub gettime
{
	local($year,$mon,$day) = @_;
	local($daynum,$time,$i);


	$daynum = 0;
	$mon = $mon - 1;

	$daynum += ($year-1)*365+int(($year-1)/4)-int(($year-1)/100)+int(($year-1)/400);

	for($i = 0; $i < $mon; $i++){
		$daynum += $monthday[$i];
		if($i == 1 && &leapyear($year)){
			$daynum++;
		}
	}

	$daynum += $day;

	$time = ($daynum - 719163) * 24 * 60 * 60;
	return ($time);
}

############################################################
# 年月日時分秒（ローカルタイム)を秒数に変換する
# 引き数：年、月、日、時、分、秒（ローカルタイム)
# 戻り値：引数に対する秒数
#
sub gettimelocal
{
	local($year,$mon,$day,$hour,$min,$sec) = @_;

	local(@epoch) = localtime(0);

	$tzmin = $epoch[2] * 60 + $epoch[1];	# minutes east of GMT

	if ($tzmin > 0) {
	    $tzmin = 24 * 60 - $tzmin;		# minutes west of GMT
	    $tzmin -= 24 * 60 if $epoch[5] == 70;	# account for the date line
	}

	local($time) = &gettime($year,$mon,$day) + $hour*60*60 + $min*60 + $sec + $tzmin*60;

	return ($time);
}

############################################################
# 閏年の判定
# 引き数：年
# 戻り値：1=閏年、0=閏年じゃない
#
sub leapyear
{
	local($year) = @_;

	if(($year % 4 == 0 && $year % 100 != 0) || $year % 400 == 0){
		return 1;
	}else{
		return 0;
	}
}

############################################################
# ２０００年問題に対応した日付けを求める
# 引き数：gettimeやtimeの戻り値
# 戻り値：年、月、日、曜日、時間、分、秒
#
sub getdatetime
{
	local($time) = @_; if($time eq ""){$time = time;}

	($sec,$min,$hour,$day,$mon,$year,$wday,$yday,$isdst) = localtime($time);

	$year = $year+1900;
	$mon = $mon+1;
#	$mon = sprintf("%02d", $mon);
#	$day = sprintf("%02d", $day);
	$wday = @wdays[$wday];
#	$hour = sprintf("%02d", $hour);
#	$min = sprintf("%02d", $min);
#	$sec = sprintf("%02d", $sec);

	return($year,$mon,$day,$wday,$hour,$min,$sec);	
}

############################################################
# ＷＥＢから送信されたフォームを読み込む
# 引き数：jcode.plの文字コード(sjis,jis,euc,etc)
# 戻り値：フォームの配列(%FORM)
#
sub read_input
{
	$charset = $_[0];
	$charset = 'euc' if ( $charset eq '' );
	local ($buffer, @pairs, $pair, $envname, $value, %FORM);

	$ENV{'REQUEST_METHOD'} =~ tr/a-z/A-Z/;
	if ($ENV{'REQUEST_METHOD'} eq "POST"){
		read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
	}else{
		$buffer = $ENV{'QUERY_STRING'};
	}
	@pairs = split(/&/, $buffer);
	foreach $pair (@pairs){
		($envname, $value) = split(/=/, $pair);
		$value =~ tr/+/ /;
		$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
		$value =~ s/</&lt;/g;
		$value =~ s/>/&gt;/g;
		$value =~ s/\r\n/<BR>/g;
		$value =~ s/\n/<BR>/g;
		$value =~ s/\t/    /g;
# for Secure Version add by mi
		$value =~ s/"/&quot;/g;
		&jcode'convert(*value, $charset);
#		&jcode'convert(*envname, $charset);
		$FORM{$envname} = $value;
	}
	%FORM;
}

############################################################
# ＷＥＢから送信されたフォームを読み込みメインルーチンへ渡す
# 引き数：jcode.plの文字コード(sjis,jis,euc,etc)
# 戻り値：フォームの配列(form{'name'})
#
sub getinputfromweb {
	%main'form = &read_input( @_ );
}

############################################################
# クッキーのデータを読み込む
# 引き数：jcode.plの文字コード(sjis,jis,euc,etc)
# 戻り値：クッキーの配列(%COOKIE)
#
sub read_cookie
{
	$charset = $_[0];
	$charset = 'euc' if ( $charset eq '' );
	local($cookies, @pairs, $pair, $cookie_name, $cookie_value, %COOKIE);

	$cookies = $ENV{'HTTP_COOKIE'};
	@pairs = split(/;\s/, $cookies);
	foreach $pair (@pairs){
		($cookie_name, $cookie_value) = split(/=/, $pair);
		$cookie_value =~ tr/+/ /;
		$cookie_value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
		&jcode'convert(*cookie_value, $charset);
		$COOKIE{$cookie_name} = $cookie_value;
	}
	%COOKIE;
}

############################################################
# クッキーのデータを読み込みメインルーチンへ渡す
# 引き数：jcode.plの文字コード(sjis,jis,euc,etc)
# 戻り値：クッキーの配列(cookie{'name'})
#
sub get_cookie{
	%main'cookie = &read_cookie( @_ );
}

############################################################
# クッキーを食べさせる
# 引き数：クッキー名、クッキーの値、削除までの日数
# 戻り値：クッキーのヘッダ
#
sub set_cookie{
	local($cookie_name, $cookie_value, $expires) = @_;
	local($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst,$result);
	
	if($expires != 0){
		($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = gmtime(time + $expires*24*60*60);
	
		$year = $year+1900;
		$sec = sprintf("%02d", $sec);
		$min = sprintf("%02d", $mihtn);
		$hour = sprintf("%02d", $hour);
	
		@week_str = ("Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat");
		$wday = @week_str[$wday];
		@month_str = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec");
		$mon = @month_str[$mon];
	
		#$gm_date = "$wday, $mday\-$mon\-$year $hour:$min:$sec GMT";
		$exp_gm_date = "expires=$wday, $mday\-$mon\-$year $hour:$min:$sec GMT";

	}else{
		#$gm_date = "Thu, 1-Jan-1980 00:00:00 GMT";
		$exp_gm_date = "";
	}

#	$result = "$cookie_name=$cookie_value; expires=$gm_date; domain=$ENV{'SERVER_NAME'}; path=$ENV{'SCRIPT_NAME'}; secure ";
#	$result = "$cookie_name=$cookie_value; expires=$gm_date; domain=$ENV{'SERVER_NAME'}";
#	$result = "$cookie_name=$cookie_value; expires=$gm_date;";
	$result = "$cookie_name=$cookie_value; $exp_gm_date;";

	print "Set-Cookie: $result\n";
}

############################################################
# クッキーを削除
# 引き数：クッキー名
# 戻り値：クッキーのヘッダ
#
sub expire_cookie{
	local($cookie_name) = @_;
	&set_cookie($cookie_name, 0, 0);
}


############################################################
# 動作内容 ：文字列の暗号化
# 引数     ：平文
# 戻り値   ：暗号
# 
sub MakeCrypt{

	local($plain) = @_; 
	local(@char,$f,$now,@saltset,$pert1,$pert2,$nsalt,$salt);

	@saltset = ('a'..'z','A'..'Z','0'..'9','.','/'); # 暗号が構成される文字群
	$now = time;
	srand(time|$$);
	$f = splice(@saltset,rand(@saltset),1) . splice(@saltset,rand(@saltset),1);
	($pert1,$pert2) = unpack("C2",$f);
	$week = $now / (60*60*24*7) + $pert1 + $pert2 - length($plain);
	$nsalt = $saltset[$week % 64] . $saltset[$now % 64];

	$result = crypt($plain,$nsalt);
	if ($result =~ /^\$1\$/) { $salt = 3; } else { $salt = 0; }
	if (crypt($plain,substr($result,$salt,2)) ne $result || $result eq ''){
		return '';
	}
	return $result;
}

############################################################
# 動作内容：スケジュールデータを時間順にソート

sub sort_data
{
	local(@datakeys);
	local(@datalist) = @_;

	foreach (@datalist){
		push(@datakeys, (split(/\t/))[9]);		# 終了「分」でソート
	}
	@datalist = @datalist[sort bydatakeys $[..$#datalist];

	@datakeys = ();
	foreach (@datalist){
		push(@datakeys, (split(/\t/))[8]);		# 終了「時」でソート
	}
	@datalist = @datalist[sort bydatakeys $[..$#datalist];

	@datakeys = ();
	foreach (@datalist){
		push(@datakeys, (split(/\t/))[7]);		# 開始「分」でソート
	}
	@datalist = @datalist[sort bydatakeys $[..$#datalist];

	@datakeys = ();
	foreach (@datalist){
		push(@datakeys, (split(/\t/))[6]);		# 開始「時」でソート
	}

	@datalist = @datalist[sort bydatakeys $[..$#datalist];
	sub bydatakeys { $datakeys[$a] <=> $datakeys[$b]; }

	return @datalist;
}
#######################################################
# URL又はメールアドレスならばリンクを張る
# 
sub inline_link { 
	local($_) = @_; 
	$_ =~ s/([^=^\"]|^)((http|ftp):[!#-9\?=A-~]+)/$1<a href=$2 target=_top>$2<\/a>/g; 
	$_ =~ s/([\w\-\_]+\@[\w\-\_\.]+)/<a href=mailto:$1>$1<\/a>/g; 
	return($_); 
}

###################################################################
# 繰り返しデータ処理　年
# 引　数:西暦,年繰返しファイル名
# 戻　値:年繰返しリスト

sub kurikaeshi_yearlyc3
{
	local($yearlydata) = @_;
	local(@yearly) = ();

	if(open(DATA,"<$yearlydata")){
		while (<DATA>) { if($_ !~ /^#/){chop; push(@yearly, $_);}}
	}

	return(@yearly);
}

###################################################################
# 繰り返しデータ処理　年
# 引　数:西暦,年繰返しファイル名
# 戻　値:年繰返しリスト

sub kurikaeshi_yearly
{
	local($year,$yearlydata,$yearlydata2) = @_;
	local($shun,$yearlysize,$yearly_mon,$yearly_day,$yearly_dat,$yearly_flag,$j,$weekday,$yearly_day_tmp);
	local(@renkyuu,@yearly_tmp,@furikae,$furikaesize,$w_youbi,$weekcnt,$cntstart_day,$cntstart_youbi,$tmpcnt);
	local(@yearly) = ();

	if(open(DATA,"<$yearlydata")){
		if($year < 2000){
			while (<DATA>) { if($_ !~ /^#/){chop; push(@yearly, $_);}}
		} else {
			while (<DATA>) { if(!/^#|体育の日|成人の日/){chop; push(@yearly, $_);}} 
		}
	}

	# 春分の日の割出し(1980年以降に適用)
	$shun = int(20.8431+0.242194*($year-1980)-int(($year-1980)/4));
	push(@yearly,"3\t$shun\t春分の日\t1");

	# 秋分の日の割出し(1980年以降に適用)
	$shuu = int(23.2488+0.242194*($year-1980)-int(($year-1980)/4));
	push(@yearly,"9\t$shuu\t秋分の日\t1");

	# 振替休日のチェック
	@furikae = ();
	$yearlysize = $#yearly;

	for($j = 0; $j <= $yearlysize; $j++){
		($yearly_mon,$yearly_day,$yearly_dat,$yearly_flag) = split(/\t/,@yearly[$j]);
		$weekday = &lib'getyoubi($year,$yearly_mon,$yearly_day);
		if ($weekday == 0 && $yearly_flag == 1 && $yearly_dat ne "憲法記念日" && $yearly_dat ne "国民の休日"){
			$yearly_day_tmp = $yearly_day + 1;
			push(@furikae,"$yearly_mon\t$yearly_day_tmp\t振替休日\t1");
		}
	}
	$furikaesize = $#furikae;
	if ($furikaesize >= 1){push(@yearly,@furikae);}

	# 改正祝日法により２０００年以降、成人の日は１月第２月曜日、体育の日は１０月第２月曜日
	# いとう氏に感謝！！

	if($year >= 2000) {
		@renkyuu = ();
		@yearly_tmp = ();
		if(open(DATA,"<$yearlydata2")){
			while (<DATA>) { if($_ !~ /^#/){chop; push(@yearly_tmp, $_);}}
			close(DATA);
		}

		for($i = 0; $i <= $#yearly_tmp; $i++){
		($yearly_mon,$weekcnt,$w_youbi,$yearly_dat,$yearly_flag) = split(/\t/,@yearly_tmp[$i]);
			if($weekcnt == 1){$cntstart_day = 1;}
			elsif($weekcnt == 2){$cntstart_day = 8;}
			elsif($weekcnt == 3){$cntstart_day = 15;}
			elsif($weekcnt == 4){$cntstart_day = 22;}
			elsif($weekcnt == 5){$cntstart_day = 29;}
			$cntstart_youbi = &lib'getyoubi($year,$yearly_mon,$cntstart_day);
			$tmpcnt = $w_youbi - $cntstart_youbi;
			if($tmpcnt < 0){
				$yearly_day_tmp = $cntstart_day + (7 + $tmpcnt);
			} else {
				$yearly_day_tmp = $cntstart_day + $tmpcnt;
			}
			push(@renkyuu,"$yearly_mon\t$yearly_day_tmp\t$yearly_dat\t$yearly_flag");
		}

		$renkyuusize = $#renkyuu;
		if($renkyuusize >= 1){push(@yearly,@renkyuu);}
	}
	return(@yearly);
}

sub kurikaeshi_monthly
{
	local(@montjly) = ();
	local($monthlydata) = @_;

	if(open(DATA,"<$monthlydata")){
		while (<DATA>) { if($_ !~ /^#/){chop; push(@monthly, $_);}}
		close(DATA);
	}
	return(@monthly);
}

sub kurikaeshi_weekly
{
	local(@weekly) = ();
	local($weeklydata) = @_;

	if(open(DATA,"<$weeklydata")){
		while (<DATA>) { if($_ !~ /^#/){chop; push(@weekly, $_);}}
		close(DATA);
	}
	return(@weekly);
}
##########################################################
# 年に一回のスケジュールの読み込み
sub getyearly
{
	local($flag) = 0;
	local($mon_day,@yearly) = @_;
	local(@yearly_dat) = ();
	local($ii);

	for($ii = 0; $ii <= $#yearly; $ii++){
		($yearly_mon,$yearly_day,$yearly_dat,$yearly_flag) = split(/\t/,@yearly[$ii]);

		if("$mon_day" eq "$yearly_mon/$yearly_day"){
			$flag += $yearly_flag;
			push(@yearly_dat,$yearly_dat);
		}
	}

	if($#yearly_dat >= 0){
		return($flag,@yearly_dat);
	} else {
		return(0);
	}
}

##########################################################
# 月に一回のスケジュールの読み込み
sub getmonthly
{
	local($flag) = 0;
	local($day,@monthly) = @_;
	local(@monthly_dat) = ();
	local($ii,$monthly_day,$monthly_hour,$monthly_minits,$monthly_dat,$monthly_flag,$shu);

	for($ii = 0; $ii <= $#monthly; $ii++){
		($monthly_day,$monthly_hour,$monthly_minits,$monthly_dat,$monthly_flag,$shu) = split(/\t/,@monthly[$ii]);
		if("$day" eq "$monthly_day"){
			$flag += $monthly_flag;
			push(@monthly_dat,join("\t",$monthly_dat,$monthly_hour,$monthly_minits,$shu));
		}
	}

	if($#monthly_dat >= 0){
		return($flag,@monthly_dat);
	} else {
		return(0);
	}
}

##########################################################
# 週に一回のスケジュールの読み込み
sub getweekly
{
	local($youbi,@weekly) = @_;

	local($flag) = 0;
	local(@weekly_dat) = ();
	local($ii);

	for($ii = 0; $ii <= $#weekly; $ii++){
		($weekly_wday,$weekly_hour,$weekly_minits,$weekly_dat,$weekly_flag) = split(/\t/,@weekly[$ii]);
		if($youbi == $weekly_wday){
			$flag += $weekly_flag;
			push(@weekly_dat,join("\t",$weekly_dat,$weekly_hour,$weekly_minits));
		}
	}
	if($#weekly_dat >= 0){
		return($flag,@weekly_dat);
	} else {
		return(0);
	}
}
######################################################
#　エラー表示
sub error_illeagal_passwd
{
	print qq(
	<H2>パスワードが間違っています。<BR>
	ブラウザの「戻る」ボタンを押して、再度パスワードを入力してください。</H2>
	);
	exit 1;
}

sub error_no_passwd
{
	print qq(
	<H2>パスワードが空欄で処理できません。<BR>
	ブラウザの「戻る」ボタンを押して、再度パスワードを入力してください。</H2>
	);
	exit 1;
}

sub error_no_passwd2
{
	print qq(
	<H2>パスワードが空欄では登録できません。<BR>
	削除時に必要ですので何かしら入力してください。<BR>
	ブラウザの「戻る」ボタンを押して、再度パスワードを入力してください。</H2>
	);
	exit 1;
}

sub error_illeagal_time
{
	print qq(
	<H2>時間設定が異常です。<BR>
	開始時間と終了時間を確認してください。<BR></H2>
	);
	exit 1;
}

sub error_cant_make_file
{
	print qq(
	<H2>データファイルを作成できません。<BR>
	ディレクトリのパーミッションを確認してください。</H2>
	);
	exit 1;
}

sub error_no_input_form
{
	print qq(
	<H2>記入されていない項目があります。<BR>
	ブラウザの「戻る」ボタンを押して、空欄を記入してください。</H2>
	);
	exit 1;
}

sub error_file_locking
{
	print qq(
	<H2>混雑しています。<BR>
	少し時間をおいてから書き込みをしてください。</H2>
	);
	exit 1;
}
sub error_make_lockfile
{
	print qq(
	<H2>ロックファイルの作成に失敗しました。<BR>
	ディレクトリのパーミッションを確認してください。</H2>
	);
	exit 1;
}
sub error_data_write
{
	print qq(
	<H2>データファイルの作成に失敗しました。<BR>
	ディレクトリのパーミッションを確認してください。</H2>
	);
	exit 1;
}
sub error_illeagal_email
{
	print "<H2>メールアドレスが正しくありません。</H2>\n";
	exit 1;
}
sub error_file_mgrp
{
	print qq(
	<H2>パスワードファイルを作成できません。<BR>
	ディレクトリのパーミッションを確認してください。</H2>
	);
	exit 1;
}

1;

