#!/usr/bin/perl
#############################################################
#
# WebCalenderC3 version 0.30
#
# 制作者：　有限会社シースリー
# ＵＲＬ：　http://www.c-3.co.jp/
# 履　歴：
# Ver 0.30  04.02/08 WebCalender2を改造しWebCalenderC3として公開
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

use lib "./mgr";
require "./mgr/webcalc3lib.cgi";
require "./mgr/lib.pl";
require "./mgr/qreki.pl";
require "./mgr/webcalconf.cgi";

&main;
exit 0;
