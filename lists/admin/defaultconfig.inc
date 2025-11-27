<?php


# default configuration. These values can be changed
# via the admin page, so you do not need to edit them here
# they are used to initialise things
# if you *do* edit them, make sure they stay in the correct format
# otherwise you will end up with parse errors and things will stop working

$defaultheader = '
<link href="styles/phplist.css" type="text/css" rel="stylesheet">

</head>
<body bgcolor="#ffffff">
<a name="top"></a>
<div align=center>
<table cellspacing=0 cellpadding=0 width=710 border=0>

<tr>
<td bgcolor="#000000" rowspan=3><img height=1 alt="" src="images/transparent.png" width=1 border=0></td>
<td bgcolor="#000000"><img height=1 alt="" src="images/transparent.png" width=708 border=0></td>
<td bgcolor="#000000" rowspan=3><img height=1 alt="" src="images/transparent.png" width=1 border=0></td>
</tr>

<tr valign="top">
<td>
<!--TOP TABLE starts-->
<table cellspacing=0 cellpadding=0 width=708 border="0" bgcolor="#ffffff">

<tr valign="top">
<td height="41" background="images/top01.png" colspan="2">
<span class="phphead"><a href="http://www.phplist.com" class="phphead"><b>PHP</b>list</a></span></td>
<td background="images/top02.png" align="left">
<font size="-2">&nbsp;<i>powered by:
</i><br />&nbsp;<b>[<a class="powered" href="http://www.php.net/" target="_new"><i>PHP</i></a>]</b> + <b>[<a class="powered" href="http://www.mysql.com/" target="_new">mySQL</a>]</b></font></td>
</tr>

<tr valign="bottom">
<td><img src="images/top03a.png" width=20 height=34 alt="" border="0"></td>
<td background="images/top03b.png" height="34"><!--hello <b>ben</b>:&nbsp;<a class="urhere" href="">you are here &gt; main admin</a>-->
<td width="132" valign="bottom" background="images/top04.png"><span class="webblermenu">phplist</span></td>
</tr>

<tr>
<td bgcolor="#000000"><img height=1 alt="" src="images/transparent.png" width=20 border=0></td>
<td bgcolor="#000000"><img height=1 alt="" src="images/transparent.png" width=576 border=0></td>
<td bgcolor="#000000"><img height=1 alt="" src="images/transparent.png" width=132 border=0></td>
</tr>

<tr valign="top">
<td>&nbsp;</td>
<td>
<br />
';

$defaultfooter = '
</td>
<td>
&nbsp;</td>
</tr>
<tr><td colspan="4">&nbsp;</td></tr>
<tr><td colspan="4">&nbsp;</td></tr>
</table>
<!--TOP TABLE ends-->

</td></tr>

<!-- main page content-->

<!-- end of main page content--><!-- bottom black line-->
<tr>
<td bgcolor="#000000" colspan=3><img height=1 alt="" src="images/transparent.png" width=1 border=0></td>
</tr>

<tr>
<td bgcolor="#000000"><img height=1 alt="" src="images/transparent.png" width=1 border=0></td>
<td bgcolor="#ff9900" class="bottom">&copy; <a href="http://tincan.co.uk" target="_tincan" class="urhere">tincan limited</a> | <a class="urhere" href="http://www.phplist.com" target="_blank">phplist</a> - version <?php echo VERSION?></td>
<td bgcolor="#000000"><img height=1 alt="" src="images/transparent.png" width=1 border=0></td>
</tr>

<tr>
<td bgcolor="#000000" colspan=3><img height=1 alt="" src="images/transparent.png" width=1 border=0></td>
</tr>

<tr>
<td colspan=3><img height=3 alt="" src="images/transparent.png" width=1 border=0></td>
</tr>

<tr>
<td colspan=3>
&nbsp;
</td>
</tr>
</tbody>
</table>

</div>
</body></html>
';

if (is_file("../config/header.inc")) {
	$fd = fopen("../config/header.inc", "r");
	$defaultheader = fread($fd, filesize("../config/header.inc"));
	fclose($fd);
}
if (is_file("../config/footer.inc")) {
	$fd = fopen("../config/footer.inc", "r");
	$defaultfooter = fread($fd, filesize("../config/footer.inc"));
	fclose($fd);
}

if (isset ($_SERVER['HTTP_HOST'])) {
	$D_website = $_SERVER['HTTP_HOST'];
} else {
	$D_website = $_SERVER['SERVER_NAME'];
}
$D_domain = $D_website;
if (preg_match("#^www\.(.*)#i", $D_domain, $regs))
	$D_domain = $regs[1];

# for starters, you want to leave this line as it is.
$default_config = array (

  # any next line has the format
  # "name" => array('value','description','type'),

  # what is your website location (url)
"website" => array (
  $D_website,
  "ウェブサイトアドレス（http://不要）",
  "text"
),

  # what is your domain (for sending emails)
"domain" => array (
  $D_domain,
  "送信元ドメイン名（あなたのドメイン名）",
  "text"
),

  # admin address is the person who is in charge of this system
"admin_address" => array (
  'webmaster@[DOMAIN]',
  "システム管理者メールアドレス",
  "text"
),

  # how often to check for new versions of PHPlist
"check_new_version" => array (
  "7",
  "新バージョンをチェックする間隔（日）",
  "text"
),

  # admin addresses are other people who receive copies of subscriptions
"admin_addresses" => array (
  '',
  "システム通知をCCで受信したい全てのメールアドレス（カンマで区切って入力）",
  "text",
  1
),

  # report address is the person who gets the reports
"report_address" => array (
  'listreports@[DOMAIN]',
  "レポート通知を受信したいメールアドレス（カンマで区切って入力）",
  "text"
),

  # where will messages appear to come from
"message_from_address" => array (
  "noreply@[DOMAIN]",
  "システム通知メールのFrom（送信者）メールアドレス",
  "text"
),

"message_from_name" => array (
  "Webmaster",
  "システム通知メールの送信者名",
  "text"
),

  # what is the reply-to on messages?
"message_replyto_address" => array (
  "noreply@[DOMAIN]",
  "システム通知メールのreply-toメールアドレス",
  "text"
),

  # if there is only one visible list, do we hide it and automatically
  # subscribe users who sign up
"hide_single_list" => array (
  "1",
  "アクティブリストが一つの場合は、アクティブリストを表示せずに
   自動的にアクティブリストに追加します (0/1)",
  "boolean"
),

  # width of a textline field
"textline_width" => array (
  "40",
  "テキストボックスの幅",
  "text"
),

  # dimensions of a textarea field
"textarea_dimensions" => array (
  "10,40",
  "テキストエリアの大きさ (行,列)",
  "text"
),

  # send copies of subscribe, update unsubscribe messages to the administrator
"send_admin_copies" => array (
  "0",
  "システム管理者へ購読、購読更新、購読解除のメッセージのコピーを送信する (0/1)",
  "boolean"
),

  # the main subscribe page, when there are multiple
"defaultsubscribepage" => array (
  1,
  "デフォルト購読ページ",
  "text"
),

  # the default template for sending an html message
"defaultmessagetemplate" => array (
  0,
  "メール送信時のデフォルトHTMLテンプレート",
  "text"
),

  ## the location of your subscribe script
  #"public_baseurl" => array("http://[WEBSITE]$pageroot/",
  #  "Base URL for public pages","text"),

  # the location of your subscribe script
"subscribeurl" => array (
  $GLOBALS['scheme'] . "://[WEBSITE]$pageroot/?p=subscribe",
  "購読ページURL",
  "text"
),

  # the location of your unsubscribe script:
"unsubscribeurl" => array (
  $GLOBALS['scheme'] . "://[WEBSITE]$pageroot/?p=unsubscribe",
  "購読解除ページURL",
  "text"
),

  #0013076: Blacklisting posibility for unknown users
  # the location of your blacklist script:
"blacklisturl" => array (
  $GLOBALS['scheme'] . "://[WEBSITE]$pageroot/?p=blacklist",
  "未知のユーザの購読解除ページURL (blacklist)",
  "text"
),

# the location of your confirm script:
"confirmationurl" => array (
  $GLOBALS['scheme'] . "://[WEBSITE]$pageroot/?p=confirm",
  "購読登録確定ページURL",
  "text"
),

  # url to change their preferences
"preferencesurl" => array (
  $GLOBALS['scheme'] . "://[WEBSITE]$pageroot/?p=preferences",
  "購読情報更新ページURL",
  "text"
),

  # url to change their preferences
"forwardurl" => array (
  $GLOBALS['scheme'] . "://[WEBSITE]$pageroot/?p=forward",
  "メール転送ページURL",
  "text"
),

  # the location of your subscribe script
  #"subscribe_baseurl" => array("http://[WEBSITE]$pageroot/",
  #  "Base URL for public pages","text"),

  # the subject of the message
"subscribesubject" => array (
  "メールマガジン本登録のお願い",
  "購読登録した際にユーザが受信するメールのタイトル",
  "text"
),

  # message that is sent when people sign up to a list
  # [LISTS] will be replaced with the list of lists they have signed up to
  # [CONFIRMATIONURL] will be replaced with the URL where a user has to confirm
  # their subscription
"subscribemessage" => array (
  '

  下記、メールマガジンへのご登録ありがとうございました。

[LISTS]

  本登録を完了するために下記URLリンクをクリックしてください。
  本登録が完了するまで、メールマガジンは配信されません。

[CONFIRMATIONURL]

　ありがとうございました。
　
　本メールにお心当たりのない方は、本メールは削除してください。

  
    ',
  "購読登録した際にユーザが受信するメール本文",
  "textarea"
),

  # subject of the message when they unsubscribe
"unsubscribesubject" => array (
  "メールマガジン購読解除のご連絡",
  "購読解除した際にユーザが受信するメールのタイトル",
  "text"
),

  # message that is sent when they unsubscribe
"unsubscribemessage" => array (
  '

  メールマガジン購読解除手続きを行いました。

　メールマガジン購読の再登録を行われたい場合は、下記URLリンクより、再度お手続きください。

　[SUBSCRIBEURL]

  ありがとうございました。

  ',
  "購読解除した際にユーザが受信するメール本文",
  "textarea"
),

  # confirmation of subscription
"confirmationsubject" => array (
  'メールマガジン本登録完了しました',
  "購読本登録完了した際にユーザが受信するメールのタイトル",
  "text"
),

  # message that is sent to confirm subscription
"confirmationmessage" => array (
  '
  
  [LISTS]
  メールマガジンへようこそ。

  本メールは、メールマガジン登録情報の更新や購読解除の際の手続きの
  ご案内になっておりますので、大切に保管して頂けますようお願いいたします。

  あなたの購読しているメールマガジンは下記の通りです。
[LISTS]

  ご登録情報の修正が必要な場合は、下記URLリンクよりお手続きください。
  [PREFERENCESURL]
  
  メールマガジンの購読を中止したい場合は、下記URLリンクよりお手続きください。
  [UNSUBSCRIBEURL]

  本登録ありがとうございました。

  
  ',
  "購読本登録が完了した際にユーザが受信するメール本文",
  "textarea"
),

  # the subject of the message sent when changing the user details
"updatesubject" => array (
  "[購読情報更新のご案内] メールマガジンご登録情報が更新されました",
  "購読情報更新の際にユーザが受信するメールのタイトル",
  "text"
),

  # the message that is sent when a user updates their information.
  # just to make sure they approve of it.
  # confirmationinfo is replaced by one of the options below
  # userdata is replaced by the information in the database
"updatemessage" => array (
  '
  メールマガジンご登録情報が更新されました。
　現在ご購読中のメールマガジンは、下記の通りです。

[LISTS]

[CONFIRMATIONINFO]

  ご登録情報は下記の通りです。

[USERDATA]

  ご購読メールマガジン、ご登録情報に誤りがある場合は、下記URLリンクより修正を
  行ってください。

[PREFERENCESURL]

  ありがとうございました。

    ',
  "購読情報更新の際にユーザが受信するメール本文",
  "textarea"
),

  # this is the text that is placed in the [!-- confirmation --] location of the above
  # message, in case the email is sent to their new email address and they have changed
  # their email address
"emailchanged_text" => array (
  '
  ご登録情報を変更された際にメールアドレスが修正されました。
  このため、メールアドレスの確認が必要となります。
  お手数ですが、下記URLリンクをクリックして、メールアドレスの変更を
  完了してください。

[CONFIRMATIONURL]

  ',
  "購読情報更新の際にメールアドレス変更が含まれる場合の新しいメールアドレスへの部分通知文",
  "textarea"
),

  # this is the text that is placed in the [!-- confirmation --] location of the above
  # message, in case the email is sent to their old email address and they have changed
  # their email address
"emailchanged_text_oldaddress" => array (
  '
  ご登録情報を変更された際にメールアドレスが修正されました。
  このため、メールアドレスの確認が必要となります。
  お手数ですが、新しいメールアドレスの受信メールをご確認の上、
  メールアドレスの変更を完了してください。
  ',
  "購読情報更新の際にメールアドレス変更が含まれる場合の古いメールアドレスへの部分通知文",
  "textarea"
),

"personallocation_subject" => array (
  'ご登録情報更新お手続きのご案内',
  "ユーザが登録情報更新手続きを求める際に送信するメールのタイトル",
  "text"
),

"personallocation_message" => array (
  '
  
ご登録情報を更新のためのお手続きをご案内します。。
下記に記載されるURLリンクより、お手続きを行ってください。
URLリンクは複数行に改行されて表示されることがありますが、全て1行のURLとして
ご利用ください。

ご登録情報の更新お手続きはこちらから
[PREFERENCESURL]

ご利用ありがとうございました。

  ',
  'ユーザが登録情報更新手続きを求める際に送信するメール本文',
  "textarea"
),

"messagefooter" => array (
  "--\n$strToUnsubscribe [UNSUBSCRIBE]\n\n$strToUpdate [PREFERENCES]\n$strForwardTitle [FORWARD]",
  "メールを送信する際のデフォルトフッタ",
  "textarea"
),

"forwardfooter" => array (
  "--\n$strForwardFooter\n\n [SUBSCRIBE]\nClick [BLACKLIST] to refuse further email from this website",

  "メールが転送される際のフッタ",
  "textarea"
),

"pageheader" => array (
  $defaultheader,
  "通常ページのヘッダ. ヘッダは必ず &lt;/head&gt; で書き始めてください。ヘッダへタグを追加できますが、titleなど基本的なヘッダタグを追加することはできません。",
  "textarea"
),

"pagefooter" => array (
  $defaultfooter,
  "通常ページのフッタ",
  "textarea"
),

"html_charset" => array (
  "iso-2022-jp",
  "HTMLメールの文字コード",
  "text"
),
"text_charset" => array (
  "iso-2022-jp",
  "テキストメールの文字コード",
  "text"
),

"html_email_style" => array (
  '
  <style type="text/css">
  body { font-size : 11px; font-family: Verdana, Arial, Helvetica, sans-serif; }
  a { font-size: 11px; color: #ff6600; font-style: normal; font-family: verdana, sans-serif; text-decoration: none; }
  a:visited { color: #666666; }
  a:hover {  text-decoration: underline; }
  p { font-weight: normal; font-size: 11px; color: #666666; font-style: normal; font-family: verdana, sans-serif; text-decoration: none; }
  h1 {font-weight: bold; font-size: 14px; color: #666666; font-style: normal; font-family: verdana, sans-serif; text-decoration: none;}
  h2 {font-weight: bold; font-size: 13px; color: #666666; font-style: normal; font-family: verdana, sans-serif; text-decoration: none;}
  h3 {font-weight: bold; font-size: 12px; color: #666666; font-style: normal; font-family: verdana, sans-serif; text-decoration: none; margin:0px; padding:0px;}
  h4 {font-weight: bold; font-size: 11px; color: #666666; font-style: normal; font-family: verdana, sans-serif; text-decoration: none; margin:0px; padding:0px;}
  hr {width : 100%; height : 1px; color: #ff9900; size:1px;}
  .forwardform {margin: 0 0 0 0; padding: 0 0 0 0;}
  .forwardinput {margin: 0 0 0 0; padding: 0 0 0 0;}
  .forwardsubmit {margin: 0 0 0 0; padding: 0 0 0 0;}
  div.emailfooter { font-size : 11px; font-family: Verdana, Arial, Helvetica, sans-serif; }
  div.emailfooter a { font-size: 11px; color: #ff6600; font-style: normal; font-family: verdana, sans-serif; text-decoration: none; }
  </style>
  ',
  "テンプレートを利用しない際のHTMLメールのスタイルシート設定",
  "textarea"
),

"alwayssendtextto" => array (
  "mail.com\nemail.com",
  "テキストメールのみ受信可能なドメイン（1行に1つのドメインを記入してください）",
  "textarea"
),
  # do not do anything with this line
"last one" => "blah"
);

if (defined("ENABLE_RSS") && ENABLE_RSS) {
  $default_config["rssthreshold"] = array (
    4,
    "RSSフィードで送る最小数",
    "text"
  );
  $default_config["rsstexttemplate"] = array (
    '
      [title]
      [description]
      URL: [link]
      ',
    "RSSフィードでのテキスト情報用テンプレート",
    "textarea"
  );
  $default_config["rsshtmltemplate"] = array (
    '<br/>
      <a href="[link]"><b>[title]</b></a><br/>
      <p>[description]</p>
      <hr/>
      ',
    "RSSフィードでのHTML情報用テンプレート",
    "textarea"
  );
  $default_config["rssthreshold"] = array (
    4,
    "RSSフィードで送る最小数",
    "text"
  );
  $default_config["rssmax"] = array (
    30,
    "RSSフィードで送る最大数",
    "text"
  );
  $default_config["rsstextseparatortemplate"] = array (
    '**** [listname] ******
    
      ',
    "RSSフィードでのテキスト情報間を区切るテンプレート",
    "textarea"
  );
  $default_config["rsshtmlseparatortemplate"] = array (
    '<br/>
      <h3>[listname]</h3>
      ',
    "RSSフィードでのHTML情報間を区切るテンプレート",
    "textarea"
  );

}

#if (USEFCK) {
$default_config["fckeditor_width"] = array (
	600,
	"FCKeditor編集エリアの幅（ピクセル）",
	"text"
);
$default_config["fckeditor_height"] = array (
	600,
	"FCKeditor編集エリアの高さ（ピクセル）",
	"text"
);
#}

########## certainly do not edit after this #########

$redfont = "<font color=\"red\">";
$efont = "</font>";

if (!TEST && REGISTER && defined("VERSION")) {
	if (ereg("dev", VERSION))
		$v = "dev";
	else
		$v = VERSION;
	$PoweredBy = '<p align=left><a href="http://www.phplist.com"><img src="http://phplist.tincan.co.uk/images/' . $v . '/power-phplist.png" width=88 height=31 title="powered by phplist" alt="powered by phplist" border="0"></a></p>';
} else
	$PoweredBy = '<center><a href="http://www.phplist.com"><img src="images/power-phplist.png" width=88 height=31 title="powered by phplist" alt="powered by phplist" border="0"></a></center>';

if (!function_exists("getconfig")) { 
	function getConfig($item) {
		global $default_config, $domain, $website, $tables;

		if ($item != 'website' && isset ($GLOBALS['config'][$item])) {
			return $GLOBALS['config'][$item];
		}
		if (!isset ($GLOBALS['config']) || !is_array($GLOBALS['config'])) {
			$GLOBALS['config'] = array ();
		}

		$hasconf = Sql_Table_Exists($tables["config"], 1);
		# correct old methods for finding public urls
		# @@@@ hmm maybe need to revert this
		/*
		if ($item == "forwardurl" || $item == "subscribeurl" || $item == "unsubscribeurl" || $item == "confirmationurl" || $item == "preferencesurl") {
		  $toget = 'public_baseurl';
		} else {
		  $toget = $item;
		}
		*/
		$toget = $item;
		if ($hasconf)
			$req = Sql_Query("select value from {$tables["config"]} where item = \"$toget\"");
		if (!Sql_Affected_Rows() || !$hasconf) {
			if (isset ($default_config[$item])) {
				$value = $default_config[$item][0];
			} else {
				$value = "";
			}
			# save the default value to the database, so we can obtain
			# the information when running from commandline
			if (Sql_Table_Exists($tables["config"]))
				saveConfig($item, $value);
			#    print "$item => $value<br/>";
		} else {
			$row = Sql_fetch_Row($req);
			$value = $row[0];
		}
		/*
		    $sep = ereg('\?',$value)?'&':'?';
		    switch ($item) {
		      case "subscribeurl":$value .= $sep.'p=subscribe';break;
		      case "unsubscribeurl":$value .= $sep.'p=unsubscribe';break;
		      case "preferencesurl":$value .= $sep.'p=preferences';break;
		      case "confirmationurl":$value .= $sep.'p=confirm';break;
		      case "forwardurl": $value .= $sep.'p=forward';break;
		    }
		*/
		$value = preg_replace('/\[DOMAIN\]/i', $domain, $value);
		$value = preg_replace('/\[WEBSITE\]/i', $website, $value);
		$value = preg_replace('/<\?=VERSION\?>/i', VERSION, $value);
		if (isset ($default_config[$item])) {
			$type = $default_config[$item][2];
		} else {
			$type = "";
		}

		if ($type == "boolean") {
			if ($value == "0") {
				$value = "false";
			}
			elseif ($value == "1") {
				$value = "true";
			}
		}
		#  print "$item => $value<br/>";
		# if this is a subpage item, and no value was found get the global one
		if (!$value && ereg(":", $item)) {
			list ($a, $b) = split(":", $item);
			return getConfig($a);
		} else {
			$GLOBALS['config'][$item] = stripslashes($value);
			return $GLOBALS['config'][$item];
		}
	}
} else {
	reset($default_config);
	while (list ($item, $values) = each($default_config)) {
		$val = getConfig($item);
		if (!isset ($val)) {
			#0013076: Blacklisting posibility for unknown users
			if ($item == 'preferencesurl' || $item == 'unsubscribeurl' || $item == 'blacklisturl' || $item == 'subscribeurl' || $item == 'forwardurl' || $item == 'confirmationurl') {
				$base = getConfig('public_baseurl');
				$sep = ereg('\?', $base) ? '&amp;' : '?';
				if (trim($base) != '') {
					switch ($item) {
						case "preferencesurl" :
							$values[0] = $base . $sep . 'p=preferences';
							break;
            case "unsubscribeurl" :
              $values[0] = $base . $sep . 'p=unsubscribe';
              break;
            #0013076: Blacklisting posibility for unknown users
            case "blacklisturl" :              
              $values[0] = $base . $sep . 'p=blacklist';
              break;
            case "subscribeurl" :
							$values[0] = $base . $sep . 'p=subscribe';
							break;
						case "forwardurl" :
							$values[0] = $base . $sep . 'p=forward';
							break;
						case "confirmationurl" :
							$values[0] = $base . $sep . 'p=confirm';
							break;
					}
				}
			}
			saveConfig($item, $values[0], 0);
		}
	}
}

function getUserConfig($item, $userid = 0) {
	global $default_config, $tables, $domain, $website;
	$hasconf = Sql_Table_Exists($tables["config"]);
	if ($hasconf)
		$req = Sql_Query("select value from {$tables["config"]} where item = \"$item\"");
	if (!Sql_Affected_Rows() || !$hasconf)
		$value = $default_config[$item][0];
	else {
		$row = Sql_fetch_Row($req);
		$value = $row[0];
	}
	# if this is a subpage item, and no value was found get the global one
	if (!$value && ereg(":", $item)) {
		list ($a, $b) = split(":", $item);
		$value = getUserConfig($a, $userid);
	}
	if ($userid) {
		$user_req = Sql_Fetch_Row_Query("select uniqid from {$tables["user"]} where id = $userid");
		$uniqid = $user_req[0];
		# parse for placeholders
		# do some backwards compatibility:
		# hmm, reverted back to old system

    $url = getConfig("unsubscribeurl");
    $sep = ereg('\?', $url) ? '&' : '?';
    $value = eregi_replace('\[UNSUBSCRIBEURL\]', $url . $sep . 'uid=' . $uniqid, $value);
		$url = getConfig("confirmationurl");
		$sep = ereg('\?', $url) ? '&' : '?';
		$value = eregi_replace('\[CONFIRMATIONURL\]', $url . $sep . 'uid=' . $uniqid, $value);
		$url = getConfig("preferencesurl");
		$sep = ereg('\?', $url) ? '&' : '?';
		$value = eregi_replace('\[PREFERENCESURL\]', $url . $sep . 'uid=' . $uniqid, $value);
	}
	$value = eregi_replace('\[SUBSCRIBEURL\]', getConfig("subscribeurl"), $value);
	$value = preg_replace('/\[DOMAIN\]/i', $domain, $value); #@ID Should be done only in one place. Combine getConfig and this one?
	$value = preg_replace('/\[WEBSITE\]/i', $website, $value);
	if ($value == "0") {
		$value = "false";
	}
	elseif ($value == "1") {
		$value = "true";
	}
	return $value;
}

# list of pages and categorisation in the system
$system_pages = array (
	"system" => array (
		"adminattributes" => "none",
		"attributes" => "none",
		"upgrade" => "none",
		"configure" => "none",
		"spage" => "owner",
		"spageedit" => "owner",
		"defaultconfig" => "none",
		"defaults" => "none",
		"initialise" => "none",
		"bounces" => "none",
		"bounce" => "none",
		"processbounces" => "none",
		"eventlog" => "none",
		"reconcileusers" => "none",
		"getrss" => "owner",
		"viewrss" => "owner",
		"purgerss" => "none",
		"setup" => "none",
		"dbcheck" => "none",
		
	),
	"list" => array (
		"list" => "owner",
		"editlist" => "owner",
		"members" => "owner"
	),
	"user" => array (
		"user" => "none",
		"users" => "none",
		"dlusers" => "none",
		"editattributes" => "none",
		"usercheck" => "none",
		"import1" => "none",
		"import2" => "none",
		"import3" => "none",
		"import4" => "none",
		"import" => "none",
		"export" => "none",
		"massunconfirm" => "none",
		
	),
	"message" => array (
		"message" => "owner",
		"messages" => "owner",
		"processqueue" => "none",
		"send" => "owner",
		"preparesend" => "none",
		"sendprepared" => "all",
		"template" => "none",
		"templates" => "none"
	),
	"clickstats" => array (
		'statsmgt' => 'owner',
		'mclicks' => 'owner',
		'uclicks' => 'owner',
		'userclicks' => 'owner',
		'mviews' => 'owner',
		'statsoverview' => 'owner',
		
	),
	"admin" => array (
		"admins" => "none",
		"admin" => "owner"
	)
);

$access_levels = array (
	0 => "none",
	1 => "all",
	2 => "view",
		#   3 => "edit",
	4 => "owner"
);
?>