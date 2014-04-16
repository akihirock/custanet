# ************************************
# HTTP Path
# ************************************
http_path = "/"
 
# ************************************
# CSS Directory
# ************************************
css_dir = "css/"
 
# ************************************
# Sass Directory
# ************************************
sass_dir = "sass/"
 
# ************************************
# Image Directory
# ************************************
images_dir = "images/"
 
# ************************************
# JavaScript Directory
# ************************************
javascripts_dir = "js/"
 
# ************************************
# Other
# ************************************
# .sass-cache���o�͂��邩�ǂ���
cache = false
 
# �N�G�X�g�ɃN�G��������t���ăL���b�V���h��
asset_cache_buster :none
 
# Sass�t�@�C�����u���E�U�Ŋm�F
sass_options = { :debug_info => false }
 
# css�̎�͌`�� 
output_style = :expanded
 
# true�ő��΃p�X�Afalse�Ő�΃p�X
relative_assets = true
 
# CSS�t�@�C����Sass�t�@�C���̉��s�ڂɋL�q���ꂽ���̂����o�͂���
line_comments = false
 
# ************************************
# Sprites
# ************************************
# Make a copy of sprites with a name that has no uniqueness of the hash.
on_sprite_saved do |filename|
  if File.exists?(filename)
    FileUtils.cp filename, filename.gsub(%r{-s[a-z0-9]{10}\.png$}, '.png')
    FileUtils.rm_rf(filename)
  end
end
 
# Replace in stylesheets generated references to sprites
# by their counterparts without the hash uniqueness.
on_stylesheet_saved do |filename|
  if File.exists?(filename)
    css = File.read filename
    File.open(filename, 'w+') do |f|
      f << css.gsub(%r{-s[a-z0-9]{10}\.png}, '.png')
    end
  end
end