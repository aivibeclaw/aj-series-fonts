<?php
/**
 * Plugin Name: AJ Series & Aaahhh Fonts Vibe — 5 Enterprise 3D Fonts & Sound of Font
 * Plugin URI:  https://fonts.aivibe.cloud
 * Description: Registers all 5 handcrafted 3D-pressed AJ Series & Aaahhh Fonts Vibe families (27 styles, 25+ languages, 28 currencies) and the Sound-of-Font phonetic typing helper in WordPress & WooCommerce.
 * Version:     3.1.0
 * Author:      Aravind Jayamohan · Aivibe Software Services Private Limited
 * Author URI:  https://www.aivibe.in
 * License:     LicenseRef-Aivibe-Open-Ecosystem-NoMod-NoResale-3.1
 */

if (!defined('ABSPATH')) {
    exit;
}

add_action('wp_enqueue_scripts', function () {
    wp_enqueue_style(
        'aj-series-aaahhh-fonts',
        'https://fonts.aivibe.cloud/css/index.css',
        array(),
        '3.1.0'
    );
});

add_action('enqueue_block_editor_assets', function () {
    wp_enqueue_style(
        'aj-series-aaahhh-fonts-editor',
        'https://fonts.aivibe.cloud/css/index.css',
        array(),
        '3.1.0'
    );
});
