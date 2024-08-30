<?php

use PHPMailer\PHPMailer\PHPMailer;
use PHPMailer\PHPMailer\SMTP;
use PHPMailer\PHPMailer\Exception;

require '../vendor/autoload.php';
include(__DIR__ . '/../a.php');
$all_banners = all_banners();
$mail = new PHPMailer(true);

if (filter_input(INPUT_POST, 'send-message', FILTER_SANITIZE_SPECIAL_CHARS) === 'da-send-message') {
    $response = $_POST['cf-turnstile-response'];
    $subject = $_POST['subject'];
    $name = $_POST['first_name'];
    $last_name = $_POST['last_name'];
    $email = $_POST['email_address'];
    $phone = $_POST['phone'];
    $user_message = $_POST['form_message'];

    if (turnstile($response)) {
        $message = /** @lang text */
            "<!DOCTYPE HTML>
<html lang='\"en\"'>
<head>
<style>
                    .ka {
                        padding: 100px 0 0 0;
                    }
            
                    .ka1 {
                        color: #20bea8;
                    }
            
                    .ka2 {
                        padding: 2% 25% 2% 25%;
                        color: #606662;
                        text-align: left;
            
                    }
            
                    .ka3 {
                        /*background-color: #20bea8;*/
                        /*padding: 10px;*/
                        /*margin: 30px;*/
                        text-decoration: none;
                        color: #fff;
                        font-weight: 700;
                        font-size: 1.3em;
                        /*text-align: left;*/
            
                    }
            
                    .ka4 {
                        background-color: #20bea8;
                        padding: 10px;
                        margin: 30px 25% 30px 25%;
                        text-decoration: none;
                        color: #fff;
                        text-align: center;
                        border-radius: 5px;
            
                    }
            
                    .ku {
                        background-color: #e4edef;
                        padding: 50px 0 50px 0;
                        box-sizing: border-box;
                        display: block;
                        font-family: \"Open Sans\", sans-serif;
                        font-size: 14px;
                        line-height: 20px;
                        color: #8d9a9d;
                        /*text-align: center;*/
            
                    }
            
                    .main-container {
                        background-color: #F6F8F9;
                        /*height: 500px;*/
                        /*padding: 50px;*/
                        text-align: center;
                    }
            
                </style>
</head>
<body class='\"\"'>
<div class='\"main-container\"'>
<div class='\"ka\"'>
<img alt='\"\"' height='\"50\"' src='\"https://www.amkamdam.com/assets/images/logo-3.png\"'/>
</div>
<div class='\"ka1\"'>
                    A prepaid credit card for the crypto community
                </div>
<br/>
<div class='\"ka2\"'>
<h3>$name $last_name</h3>
<p>$user_message</p>
<p>Instant Messenger: $phone</p>
<br/>
</div>
<div class='\"ku\"'>
<img alt='\"\"' src='\"https://kumpenot.com/media/img/foot.png\"'/>
<p class='\"footer-text\"'>No. 5, 17/F Bonham Trade Centre, 50 Bonham Strand, Sheung Wan, Hong Kong</p>
<p class='\"footer-text\"'>52-60 Tabernacle Street, London, United Kingdom, EC2A 4NJ</p>
<p class='\"footer-copyright\"'>© 2018-2019 <a href='\"index.htm\"'>kumpenot Ltd </a></p>
</div>
</div>
</body>
</html>
            ";

        try {

            //Server settings
            $mail-&gt;SMTPDebug = SMTP::DEBUG_OFF;                      //Enable verbose debug output: DEBUG_SERVER
            $mail-&gt;isSMTP();                                            //Send using SMTP
            $mail-&gt;Host = 'smtp.ionos.co.uk';                     //Set the SMTP server to send through
            $mail-&gt;SMTPAuth = true;                                   //Enable SMTP authentication
            $mail-&gt;Username = 'support@amkamdam.com';                     //SMTP username
            $mail-&gt;Password = 'Zaichik1.&amp;';                               //SMTP password
            $mail-&gt;SMTPSecure = PHPMailer::ENCRYPTION_STARTTLS;            //Enable implicit TLS encryption
            $mail-&gt;Port = 587;                                    //TCP port to connect to; use 587 if you have set `SMTPSecure = PHPMailer::ENCRYPTION_STARTTLS`

            //Recipients
            $mail-&gt;setFrom($email, $name);
            $mail-&gt;addAddress('support@amkamdam.com');     //Add a recipient
//    $mail-&gt;addAddress('ellen@example.com');               //Name is optional
//        $mail-&gt;addReplyTo('support@amkamdam.com', 'support');
//        $mail-&gt;addCC('alexlisak@hotmail.com');
//    $mail-&gt;addBCC('bcc@example.com');

            //Attachments
//        $mail-&gt;addAttachment('../assets/images/125.png');         //Add attachments
//    $mail-&gt;addAttachment('/tmp/image.jpg', 'new.jpg');    //Optional name

            //Content
            $mail-&gt;isHTML(true);                                  //Set email format to HTML
            $mail-&gt;Subject = $subject;
            $mail-&gt;Body = $message;
//        $mail-&gt;AltBody = 'This is the body in plain text for non-HTML mail clients';

            $mail-&gt;send();
//            echo 'Message has been sent huy';
        } catch (Exception $e) {
//            echo "Message could not be sent. Mailer Error: {$mail-&gt;ErrorInfo}";
        }
        $err = urlencode("You have sent message successfully.");
        header("Location: /contact/?err=$err");
        exit ();
    } else {
        $err = urlencode("Try again.");
        header("Location: /contact/?err=$err");
        exit ();
    }
}

?&gt;


<!DOCTYPE html>

<html lang="en">
<head>
<title id="dynamicTitle">kumpeton</title>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1" name="viewport"/>
<meta content="Crypto News: Latest Cryptocurrency News, Bitcoin News, Ethereum News and Price Data" property="og:title"/>
<meta content="We deliver up-to-date, breaking crypto news about the latest Bitcoin, Ethereum, Blockchain, NFTs, and Altcoin trends and happenings." name="og:description"/>
<script defer="" src="/assets/js/frontend.js"></script>
<link href="/assets/css/frontend.css" rel="stylesheet"/>
<link href="/assets/images/favicon.png" rel="shortcut icon"/>
<script>
        window.trans = {
            ago: "ago",
            ago_long: "minute, minutes, hour, hours, day, days",
            time_seconds_ago: "[time] [seconds] [ago]",
            time_minutes_ago: "[time] [minutes] [ago]",
            time_hours_ago: "[time] [hours] [ago]",
            time_days_ago: "[time] [days] [ago]",
        }

    </script>
<script>
        window.sid = 1;
    </script>
<script async="" defer="" src="https://challenges.cloudflare.com/turnstile/v0/api.js"></script>
<link href="https://cdn.jsdelivr.net/gh/orestbida/cookieconsent@v2.9.2/dist/cookieconsent.css" rel="stylesheet"/>
</head>
<body>
<header class="header" id="header">
<a class="header__logo" href="/">
<img alt="Crypto News" src="/assets/images/logo.svg"/>
</a>
<div class="header-menu">
<div class="header-menu__trigger d-none d-lg-flex">
<svg height="15" viewbox="0 0 12 7" width="20" xmlns="http://www.w3.org/2000/svg">
<g fill-rule="evenodd">
<path d="M0 3.999L12 3.999 12 2.999 0 2.999zM0 7L12 7 12 6 0 6zM0 1L12 1 12 0 0 0z" fill="#ffffff"></path>
</g>
</svg>
</div>
<div class="header-menu__dropdown" hidden="" id="dropdown-menu">
<div class="container header-menu__dropdown-container">
<div class="row">
<div class="col-12 col-lg-2">
<div class="header-links__dropdown-list">
<div class="header-menu__dropdown-heading">
<a class="heading" href="/news/">News</a><span>+</span>
</div>
<ul class="header-menu__dropdown-children">
<li><a href="/news/bitcoin-news/">Bitcoin News</a></li>
<li><a href="/news/ethereum-news/">Ethereum News</a></li>
<li><a href="/news/nft-news/">NFT News</a></li>
<li><a href="/news/defi-news/">DeFi News</a></li>
<li><a href="/news/altcoin-news/">Altcoin News</a></li>
<li><a href="/news/blockchain-news/">Blockchain News</a></li>
<li><a href="/news/press-releases/">Press Releases</a></li>
<li><a href="/news/sponsored/">Sponsored</a></li>
<li><a href="/news/industry-talk/">Industry Talk</a></li>
<li><a href="/news/ico-news/">ICO news</a></li>
<li><a href="/news/finance-news/">Finance News</a></li>
<li><a href="/news/technology-news/">Technology News</a></li>
</ul>
</div>
</div>
<div class="col-12 col-lg-2">
<div class="header-links__dropdown-list">
<div class="header-menu__dropdown-heading">
<a class="heading" href="/exclusives/">Exclusives</a><span>+</span>
</div>
<ul class="header-menu__dropdown-children">
<li><a href="/exclusives/features/">Features</a></li>
<li><a href="/exclusives/opinions/">Opinions</a></li>
<li><a href="/exclusives/people/">People In Crypto</a></li>
</ul>
</div>
</div>
<div class="col-12 col-lg-2">
<div class="header-links__dropdown-list">
<div class="header-menu__dropdown-heading">
<a class="heading" href="/guides/">Guides</a><span>+</span>
</div>
<ul class="header-menu__dropdown-children">
<li><a href="/guides/bitcoin/">Bitcoin</a></li>
<li><a href="/guides/ethereum/">Ethereum</a></li>
<li><a href="/guides/nft/">NFT</a></li>
<li><a href="/guides/defi-guides/">Defi Guides</a></li>
<li><a href="/guides/altcoins/">Altcoins</a></li>
<li><a href="/guides/blockchain/">Blockchain</a></li>
<li><a href="/guides/cryptocurrency/">Cryptocurrency</a></li>
<li><a href="/guides/icos/">ICOs / STOs / IEOs</a></li>
</ul>
</div>
</div>
<div class="col-12 col-lg-2">
<div class="header-links__dropdown-list">
<div class="header-menu__dropdown-heading">
<a class="heading" href="/reviews/exchanges/">Exchanges</a><span></span>
</div>
<div class="header-menu__dropdown-heading">
<a class="heading" href="/coins/">Market Cap</a><span></span>
</div>
<div class="header-menu__dropdown-heading">
<a class="heading" href="/news/press-releases/">Press Releases</a><span></span>
</div>
<div class="header-menu__dropdown-heading">
<a class="heading" href="/news/industry-talk/">Industry Talk</a><span></span>
</div>
<div class="header-menu__dropdown-heading">
<a class="heading" href="/exclusives/opinions/">Opinions</a><span></span>
</div>
</div>
</div>
<div class="col-12 col-lg-2">
<div class="header-links__dropdown-list">
<div class="header-menu__dropdown-heading">
<a class="heading" href="#">Recommended</a><span>+</span>
</div>
<ul class="header-menu__dropdown-children">
<li>
<a href="/news/best-crypto-to-buy.htm"> Best crypto to buy now</a>
</li>
<li>
<a href="/news/best-crypto-presales.htm"> Best crypto presales to invest in</a>
</li>
<li>
<a href="/news/new-cryptocurrency.htm"> New cryptocurrency</a>
</li>
<li>
<a href="/news/next-cryptocurrency-to-explode.htm"> Next cryptocurrency to explode</a>
</li>
<li>
<a href="/news/best-crypto-icos.htm"> Best crypto icos</a>
</li>
<li>
<a href="/news/crypto-launches.htm"> Crypto launches</a>
</li>
<li>
<a href="/news/best-bitcoin-betting-sites.htm"> Crypto betting</a>
</li>
<li>
<a href="/news/best-bitcoin-casinos.htm"> Bitcoin casinos</a>
</li>
<li>
<a href="/news/best-bitcoin-gambling-sites.htm"> Bitcoin gambling sites</a>
</li>
</ul>
</div>
</div>
</div>
</div>
</div>
</div>
<div class="header-links d-none d-lg-flex">
<ul class="menu_header">
<li></li>
<li>
<a href="/news/">News
                    <span class="menu_icon"></span></a><span class="menu_icon mob"></span>
<ul class="sub-menu">
<li><a href="/news/bitcoin-news/">Bitcoin News</a></li>
<li><a href="/news/ethereum-news/">Ethereum News</a></li>
<li><a href="/news/nft-news/">NFT News</a></li>
<li><a href="/news/defi-news/">DeFi News</a></li>
<li><a href="/news/altcoin-news/">Altcoin News</a></li>
<li><a href="/news/blockchain-news/">Blockchain News</a></li>
<li><a href="/news/press-releases/">Press Releases</a></li>
<li><a href="/news/sponsored/">Sponsored</a></li>
<li><a href="/news/industry-talk/">Industry Talk</a></li>
<li><a href="/news/ico-news/">ICO news</a></li>
<li><a href="/news/finance-news/">Finance News</a></li>
<li><a href="/news/technology-news/">Technology News</a></li>
</ul>
</li>
<li>
<a href="/exclusives/">Exclusives
                    <span class="menu_icon"></span></a><span class="menu_icon mob"></span>
<ul class="sub-menu">
<li><a href="/exclusives/features/">Features</a></li>
<li><a href="/exclusives/opinions/">Opinions</a></li>
<li><a href="/exclusives/people/">People In Crypto</a></li>
</ul>
</li>
<li>
<a href="/guides/">Guides
                    <span class="menu_icon"></span></a><span class="menu_icon mob"></span>
<ul class="sub-menu">
<li><a href="/guides/bitcoin/">Bitcoin</a></li>
<li><a href="/guides/ethereum/">Ethereum</a></li>
<li><a href="/guides/nft/">NFT</a></li>
<li><a href="/guides/defi-guides/">Defi Guides</a></li>
<li><a href="/guides/altcoins/">Altcoins</a></li>
<li><a href="/guides/blockchain/">Blockchain</a></li>
<li><a href="/guides/cryptocurrency/">Cryptocurrency</a></li>
<li><a href="/guides/icos/">ICOs / STOs / IEOs</a></li>
</ul>
</li>
<li>
<a href="/reviews/exchanges/">Exchanges
                </a>
</li>
<li>
<a href="/coins/">Market Cap</a>
</li>
<li>
<a href="/news/press-releases/">Press Releases</a>
</li>
<li>
<a href="/news/industry-talk/">Industry Talk</a>
</li>
<li>
<a href="/exclusives/opinions/">Opinions</a>
</li>
<li>
<a href="#">Recommended
                    <span class="menu_icon"></span></a><span class="menu_icon mob"></span>
<ul class="sub-menu">
<li>
<a href="/news/best-crypto-to-buy.htm"> Best crypto to buy now</a>
</li>
<li>
<a href="/news/best-crypto-presales.htm"> Best crypto presales to invest in</a>
</li>
<li>
<a href="/news/new-cryptocurrency.htm"> New cryptocurrency</a>
</li>
<li>
<a href="/news/next-cryptocurrency-to-explode.htm"> Next cryptocurrency to explode</a>
</li>
<li>
<a href="/news/best-crypto-icos.htm"> Best crypto icos</a>
</li>
<li>
<a href="/news/crypto-launches.htm"> Crypto launches</a>
</li>
<li>
<a href="/news/best-bitcoin-betting-sites.htm"> Crypto betting</a>
</li>
<li>
<a href="/news/best-bitcoin-casinos.htm"> Bitcoin casinos</a>
</li>
<li>
<a href="/news/best-bitcoin-gambling-sites.htm"> Bitcoin gambling sites</a>
</li>
</ul>
</li>
</ul>
</div>
<div class="header-search">
<div class="header-menu__trigger d-md-none">
<svg height="7" viewbox="0 0 12 7" width="12" xmlns="http://www.w3.org/2000/svg">
<g fill-rule="evenodd">
<path d="M0 3.999L12 3.999 12 2.999 0 2.999zM0 7L12 7 12 6 0 6zM0 1L12 1 12 0 0 0z" fill="#ffffff"></path>
</g>
</svg>
</div>
<div class="header-search__trigger">
<svg height="14" viewbox="0 0 14 14" width="14" xmlns="http://www.w3.org/2000/svg">
<path d="M6 11c-2.757 0-5-2.243-5-5 0-1.198.441-2.284 1.146-3.146.212-.26.448-.495.708-.708C3.716 1.441 4.802 1 6 1c2.757 0 5 2.243 5 5 0 1.198-.441 2.284-1.146 3.146-.212.26-.448.496-.708.708C8.284 10.559 7.198 11 6 11zm4.579-1.128C11.464 8.827 12 7.477 12 6c0-3.313-2.687-6-6-6-1.477 0-2.827.536-3.872 1.421-.255.216-.491.452-.707.707C.536 3.173 0 4.523 0 6c0 3.313 2.687 6 6 6 1.477 0 2.827-.536 3.872-1.421L13.293 14l.707-.707-3.421-3.421z" fill="#212121" fill-rule="evenodd"></path>
</svg>
</div>
<form action="/search/" class="header-search__form">
<input aria-label="search" class="remove-outline" name="q" placeholder="What are you searching for?" type="search"/>
<div class="header-search__close">
<svg id="Capa_1" version="1.1" viewbox="0 0 512 512" x="0px" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" y="0px">
<g>
<polygon points="512,28.308 483.692,0 256,227.692 28.308,0 0,28.308 227.692,256 0,483.692 28.308,512 256,284.308 483.692,512
    512,483.692 284.308,256"></polygon>
</g>
</svg>
</div>
</form>
</div>
</header>
<div class="main">
<main>
<div class="container">
<div class="breadcrumbs mb-20">
<a href="/">Kumkanot</a>
<a href="/contact/">Contact Us</a>
</div>
<div class="mb-80">
<h1 class="scrollspy" id="about-us"> Contact Us</h1>
<div class="layout-size">
<p>Kumkanot.com offers original coverage of the global blockchain and cryptocurrency news, provides opinions, reviews, guides, introduces to Crypto people with an aim to help the general public understand and successfully use these technologies now and in the future. </p>
<p>We believe that the most important thing in the Blockchain revolution is the ability of people to understand and embrace the change. Our journalism standards - impartiality, truthfulness, transparency, and accuracy - will help you navigate this extremely dynamic world.</p>
<p>Join us in this journey, as there are millions of things to learn and understand. The change happens by bringing all the voices together. </p>
<p>Kumkanot.com is backed by Antanas Guoga, ultimate blockchain enthusiast, founder of the International Blockchain Centre in Vilnius, Lithuania, entrepreneur and former Member of the European Parliament. Guoga is also known as TonyG for his poker acumen, both as world-caliber player and founder of pokernews.com (sold in 2014).</p>
</div>
</div>
</div>
<div class="vapp" data-v-app="">
<section class="container mb-60">
<div class="row">
<div class="col-12 col-md-8 offset-lg-1 col-lg-7 offset-xl-2 col-xl-6" id="formblock">
<form action="/contact/" class="contact-form mb-40" id="ContactForm" method="post" novalidate="">
<div class="row">
<input name="send-message" type="hidden" value="da-send-message"/>
<div class="col-12 col-md-6" data-v-a14ff93e="" value=""><input data-v-a14ff93e="" name="first_name" placeholder="First name*" type="text"/><span class="error-msg" data-v-a14ff93e=""></span></div>
<div class="col-12 col-md-6" data-v-a14ff93e="" value=""><input data-v-a14ff93e="" name="last_name" placeholder="Last name*" type="text"/><span class="error-msg" data-v-a14ff93e=""></span></div>
<div class="col-12 col-md-6" data-v-a14ff93e="" value=""><input data-v-a14ff93e="" name="email_address" placeholder="Email Address*" type="text"/><span class="error-msg" data-v-a14ff93e=""></span></div>
<div class="col-12 col-md-6" data-v-a14ff93e="" value=""><input data-v-a14ff93e="" name="phone" placeholder="Phone number" type="text"/><span class="error-msg" data-v-a14ff93e=""></span></div>
<div class="col-12" data-v-a14ff93e="" value=""><input data-v-a14ff93e="" name="subject" placeholder="Subject*" type="text"/><span class="error-msg" data-v-a14ff93e=""></span></div>
<div class="col-12" data-v-772218ee=""><textarea data-v-772218ee="" name="form_message" placeholder="Your message*" rows="3">
        </textarea><span class="error-msg" data-v-772218ee=""></span></div><!-- -->
<div class="col-12">
<div class="contact-form__consent fs-12 mb-30">By submitting you agree to the processing of personal data. Read our <a href="/privacy-policy.htm">Privacy Policy</a></div>
</div>
<div class="col-12">
<div class="checkbox mb-3" style="margin: 5px 0 5px 0">
<div class="cf-turnstile" data-sitekey="&lt;?= SITE_KEY ?&gt;" data-theme="light"></div>
</div>
</div>
<div class="col-12">
<button class="button-more button-more--big button-more--gradient remove-outline" type="submit">Submit Form
                                        <svg height="6" viewbox="0 0 20 6" width="20" xmlns="http://www.w3.org/2000/svg">
<path d="M6 0L1 5 0 6 1.414 6 19.999 6 19.999 5 2.413 5 6 1.415z" fill="#6C7473" fill-rule="evenodd" transform="matrix(-1 0 0 1 19.999 0)"></path>
</svg>
</button>
</div>
</div>
</form>
</div>
<div class="col-12 col-md-4 offset-xl-1 col-xl-3 align-self-center">
<div class="contact-sidebar nowrap">
<div class="mb-30">
<div class="d-inline-block mr-10 align-top">
<svg height="12" viewbox="0 0 12 12" width="12" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
<g transform="translate(-1095 -1243) translate(295 1103) translate(770 35) translate(30 100) translate(0 5) translate(0 2)">
<path d="M11.063 6.797c0 .13-.106.234-.235.234H1.172c-.13 0-.234-.105-.234-.234V1.321l4.81 3.06c.154.097.35.097.503 0l4.811-3.06v5.476zM9.918.938L6 3.43 2.08.94h7.84zM10.83 0H1.17C.531 0 0 .521 0 1.172v5.625C0 7.443.525 7.97 1.17 7.97h9.658c.646 0 1.17-.526 1.17-1.172V1.172C12 .53 11.476 0 10.83 0z" fill="#FFF"></path>
</g>
</svg>
</div>
<a class="d-inline-block" href="mailto:support@amkamdam.com">support@amkamdam.com</a></div>
<div class="mb-30">
<div class="d-inline-block">Amkamdad LTD <br/>52-60 Tabernacle Street<br/>London<br/>United Kingdom<br/>EC2A 4NJ<br/></div>
</div>
</div>
</div>
</div>
</section>
</div>
</main>
</div>
<footer class="footer">
<div class="container">
<div class="footer-top pt-60 pb-30">
<div class="row">
<div class="col-12 col-lg-5 col-xl-4 mb-lg-0 text-center text-md-left">
<div class="d-lg-flex mb-40">
<div class="footer-links d-md-inline-block text-center text-md-left align-self-center">
<a class="mr-20" href="/terms-and-conditions.htm">Terms &amp; Conditions</a>
<a class="mr-20" href="/about-us.htm">About Us</a>
<a class="mr-20" href="/contact/">Contact Us</a>
<a class="mr-20" href="/privacy-policy.htm">Privacy Policy</a>
<a class="mr-20" href="/disclaimer.htm">Disclaimer</a>
</div>
</div>
<div class="footer-tags d-none d-md-block">
</div>
</div>
<div class="col-12 col-lg-7 col-xl-8 footer-links text-md-left">
<div class="row d-none d-md-flex" style="justify-content: flex-end">
<div class="col-12 col-lg-2">
<div class="header-menu__dropdown-heading">
<a class="mb-10 heading" href="/news/"><b>News</b></a><span>+</span>
</div>
<div class="menu-list-links header-menu__dropdown-children">
<a href="/news/bitcoin-news/">Bitcoin News</a><br/>
<a href="/news/ethereum-news/">Ethereum News</a><br/>
<a href="/news/nft-news/">NFT News</a><br/>
<a href="/news/defi-news/">DeFi News</a><br/>
<a href="/news/altcoin-news/">Altcoin News</a><br/>
<a href="/news/blockchain-news/">Blockchain News</a><br/>
<a href="/news/press-releases/">Press Releases</a><br/>
<a href="/news/sponsored/">Sponsored</a><br/>
<a href="/news/industry-talk/">Industry Talk</a><br/>
<a href="/news/ico-news/">ICO news</a><br/>
<a href="/news/finance-news/">Finance News</a><br/>
<a href="/news/technology-news/">Technology News</a><br/>
</div>
</div>
<div class="col-12 col-lg-2">
<div class="header-menu__dropdown-heading">
<a class="mb-10 heading" href="/exclusives/"><b>Exclusives</b></a><span>+</span>
</div>
<div class="menu-list-links header-menu__dropdown-children">
<a href="/exclusives/features/">Features</a><br/>
<a href="/exclusives/opinions/">Opinions</a><br/>
<a href="/exclusives/people/">People In Crypto</a><br/>
</div>
</div>
<div class="col-12 col-lg-2">
<div class="header-menu__dropdown-heading">
<a class="mb-10 heading" href="/guides/"><b>Guides</b></a><span>+</span>
</div>
<div class="menu-list-links header-menu__dropdown-children">
<a href="/guides/bitcoin/">Bitcoin</a><br/>
<a href="/guides/ethereum/">Ethereum</a><br/>
<a href="/guides/nft/">NFT</a><br/>
<a href="/guides/defi-guides/">Defi Guides</a><br/>
<a href="/guides/altcoins/">Altcoins</a><br/>
<a href="/guides/blockchain/">Blockchain</a><br/>
<a href="/guides/cryptocurrency/">Cryptocurrency</a><br/>
<a href="/guides/icos/">ICOs / STOs / IEOs</a><br/>
</div>
</div>
<div class="col-12 col-lg-2">
<div class="header-menu__dropdown-heading">
<a class="mb-10 heading" href="#"><b>Recommended</b></a><span>+</span>
</div>
<div class="menu-list-links header-menu__dropdown-children">
<a href="/news/best-crypto-to-buy.htm"> Best crypto to buy now </a>
<a href="/news/best-crypto-presales.htm"> Best crypto presales to invest in </a>
<a href="/news/new-cryptocurrency.htm"> New cryptocurrency </a>
<a href="/news/next-cryptocurrency-to-explode.htm"> Next cryptocurrency to explode </a>
<a href="/news/best-crypto-icos.htm"> Best crypto icos </a>
<a href="/news/crypto-launches.htm"> Crypto launches </a>
<a href="/news/best-bitcoin-betting-sites.htm"> Crypto betting </a>
<a href="/news/best-bitcoin-casinos.htm"> Bitcoin casinos </a>
<a href="/news/best-bitcoin-gambling-sites.htm"> Bitcoin gambling sites </a>
</div>
</div>
<div class="col-lg-2">
<div class="">
<div class="header-menu__dropdown-heading"><a class="heading" href="/editors/">Contributors</a></div>
<div class="header-menu__dropdown-heading"><a class="heading" href="/reviews/exchanges/">Exchanges</a></div>
<div class="header-menu__dropdown-heading"><a class="heading" href="/coins/">Market Cap</a></div>
<div class="header-menu__dropdown-heading"><a class="heading" href="/news/press-releases/">Press Releases</a></div>
<div class="header-menu__dropdown-heading"><a class="heading" href="/news/industry-talk/">Industry Talk</a></div>
<div class="header-menu__dropdown-heading"><a class="heading" href="/exclusives/opinions/">Opinions</a></div>
</div>
</div>
</div>
<div class="row d-block d-md-none footer_menu_mob">
<div class="header-menu__dropdown-heading">
<a class="mb-10 heading" href="/news/"><b>News</b></a>
</div>
<div class="menu-list-links header-menu__dropdown-children">
<a href="/news/bitcoin-news/">Bitcoin News</a><br/><a href="/news/ethereum-news/">Ethereum News</a><br/><a href="/news/nft-news/">NFT News</a><br/><a href="/news/defi-news/">DeFi News</a><br/><a href="/news/altcoin-news/">Altcoin News</a><br/><a href="/news/blockchain-news/">Blockchain News</a><br/><a href="/news/press-releases/">Press Releases</a><br/><a href="/news/sponsored/">Sponsored</a><br/><a href="/news/industry-talk/">Industry Talk</a><br/><a href="/news/ico-news/">ICO news</a><br/><a href="/news/finance-news/">Finance News</a><br/><a href="/news/technology-news/">Technology News</a><br/></div>
<div class="header-menu__dropdown-heading">
<a class="mb-10 heading" href="/exclusives/"><b>Exclusives</b></a>
</div>
<div class="menu-list-links header-menu__dropdown-children">
<a href="/exclusives/features/">Features</a><br/><a href="/exclusives/opinions/">Opinions</a><br/><a href="/exclusives/people/">People In Crypto</a><br/></div>
<div class="header-menu__dropdown-heading">
<a class="mb-10 heading" href="/guides/"><b>Guides</b></a>
</div>
<div class="menu-list-links header-menu__dropdown-children">
<a href="/guides/bitcoin/">Bitcoin</a><br/><a href="/guides/ethereum/">Ethereum</a><br/><a href="/guides/nft/">NFT</a><br/><a href="/guides/defi-guides/">Defi Guides</a><br/><a href="/guides/altcoins/">Altcoins</a><br/><a href="/guides/blockchain/">Blockchain</a><br/><a href="/guides/cryptocurrency/">Cryptocurrency</a><br/><br/><a href="/guides/icos/">ICOs / STOs / IEOs</a><br/><br/>
</div>
<div class="header-menu__dropdown-heading">
<a class="mb-10 heading" href="#"><b>Recommended</b></a>
</div>
<div class="menu-list-links header-menu__dropdown-children">
                            [{"url":"https:\/\/kumkanot.com\/news\/best-crypto-to-buy.htm","name":"Best crypto to buy now","children":[]}]<br/>[{"url":"https:\/\/kumkanot.com\/news\/best-crypto-presales.htm","name":"Best crypto presales to invest in","children":[]}]<br/>[{"url":"https:\/\/kumkanot.com\/news\/new-cryptocurrency.htm","name":"New cryptocurrency","children":[]}]<br/>[{"url":"https:\/\/kumkanot.com\/news\/next-cryptocurrency-to-explode.htm","name":"Next cryptocurrency to
                            explode","children":[]}]<br/>[{"url":"https:\/\/kumkanot.com\/news\/best-crypto-icos.htm","name":"Best crypto icos","children":[]}]<br/>[{"url":"https:\/\/kumkanot.com\/news\/crypto-launches.htm","name":"Crypto launches","children":[]}]<br/>[{"url":"https:\/\/kumkanot.com\/news\/best-bitcoin-betting-sites.htm","name":"Crypto betting","children":[]}]<br/>[{"url":"https:\/\/kumkanot.com\/news\/best-bitcoin-casinos.htm","name":"Bitcoin
                            casinos","children":[]}]<br/>[{"url":"https:\/\/kumkanot.com\/news\/best-bitcoin-gambling-sites.htm","name":"Bitcoin gambling sites","children":[]}]<br/></div>
<div class="menu-list-links header-menu__dropdown-children">
<a class="mb-10 heading" href="/editors/">
<b>Contributors</b>
</a>
<a class="mb-10 heading" href="/reviews/exchanges/">
<b>Exchanges</b>
</a>
<a class="mb-10 heading" href="/coins/">
<b>Market Cap</b>
</a>
<a class="mb-10 heading" href="/news/press-releases/"><b>Press Releases</b></a>
<a class="mb-10 heading" href="/news/industry-talk/"><b>Industry Talk</b></a>
<a class="mb-10 heading" href="/exclusives/opinions/"><b>Opinions</b></a>
</div>
</div>
</div>
<div class="col-12 col-lg-5 col-xl-4 mb-lg-0 text-center d-md-none d-block mt-20">
<div class="footer-tags">
</div>
</div>
</div>
</div>
<div class="footer-bottom pt-30 pb-30">
<div class="row">
<div class="col-12 col-md-6 text-center text-md-left mb-20 mb-md-0">
<div class="fs-12 c-light-grey">© 2023 kumkanot. All rights reserved</div>
</div>
<div class="col-12 col-md-6 text-center text-md-right">
</div>
</div>
</div>
</div>
</footer>
<div class="modal" id="newsletter-modal">
<div class="modal__content text-white">
<div class="close__icon hide-modal" data-id="newsletter-modal">X</div>
</div>
</div>
<script src="https://cdn.jsdelivr.net/gh/orestbida/cookieconsent@v2.9.2/dist/cookieconsent.js"></script>
<script defer="" src="/assets/js/cookieconsent-init.js"></script>
</body>
</html>
