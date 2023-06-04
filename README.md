# Danbooru Tag Formatter
Automatically format tags for use with Stable Diffusion models.

This is a Python script that formats tags from various inputs for use with Stable Diffusion models. The script can accept either a danbooru post URL, a file containing tags, or unformatted tags themselves.

If given a URL, the script uses the pybooru library to extract the tags associated with the post. It then formats the tags by replacing underscores with spaces and adding commas between tags.

If given a file, the script reads through each line of the file and formats the tags in the same way as for URLs. If the file contains additional URLs or file paths, the script will also recursively process them.

Usage: tag_formatter.py <input>

## Examples

### URL
#### Command
```
python tag_formatter.py https://danbooru.donmai.us/posts/6087730
```
#### Output
```
Detected as a URL: https://danbooru.donmai.us/posts/6087730
Post ID: 6087730
Formatted tags: 1boy, absurdres, arm behind back, chinese clothes, dress, fire, flower, glowing, hanfu, highres, hua cheng, long hair, looking at another, mumuda13531, red flower, red rose, rose, smoke, string, string of fate, tian guan ci fu, wedding dress, xie lian
```

### Unformatted tags
#### Command
```
python tag_formatter.py "1girl bangs belt_collar blue_bow blue_eyes blue_ribbon bow collar dress flower frilled_dress frills hair_flower hair_ornament happy_birthday horns long_hair long_sleeves looking_at_viewer magic pink_flower pink_ribbon ribbon sheep_horns smile solo white_dress white_hair white_headdress"
```
#### Output
```
Tags detected: 1girl bangs belt_collar blue_bow blue_eyes blue_ribbon bow collar dress flower frilled_dress frills hai...
Formatted tags: 1girl, bangs, belt collar, blue bow, blue eyes, blue ribbon, bow, collar, dress, flower, frilled dress, frills, hair flower, hair ornament, happy birthday, horns, long hair, long sleeves, looking at viewer, magic, pink flower, pink ribbon, ribbon, sheep horns, smile, solo, white dress, white hair, white headdress
```

### 3 Nested files
#### Command
```
python tag_formatter.py C:\Users\admin\Documents\tag_formatter_test\test_input.txt
```
#### Output
```
[BASE FILE] (test_input.txt) Detected as a URL: https://danbooru.donmai.us/posts/6087459
[BASE FILE] (test_input.txt) Post ID: 6087459
[BASE FILE] (test_input.txt) Nested file detected: C:\Users\admin\Documents\tag_formatter_test\test_input_2.txt
[NESTED FILE] (test_input_2.txt) Detected as a URL: https://danbooru.donmai.us/posts/6087739
[NESTED FILE] (test_input_2.txt) Post ID: 6087739
[NESTED FILE] (test_input_2.txt) Nested file detected: C:\Users\admin\Documents\tag_formatter_test\test_input_3.txt
[NESTED FILE] (test_input_3.txt) Tags detected: rokugou_daisuke touhou goutokuji_mike 1girl animal_ears barefoot bell blush cat_ears cat_tail closed_ey...
[NESTED FILE] (test_input_3.txt) Formatted tags saved to: C:\Users\admin\Documents\tag_formatter_test\test_input_3_formatted.txt
[NESTED FILE] (test_input_2.txt) Formatted tags saved to: C:\Users\admin\Documents\tag_formatter_test\test_input_2_formatted.txt
[BASE FILE] (test_input.txt) Tags detected: reitou_mkn hololive nekomata_okayu onigirya_(nekomata_okayu) absurdres commentary_request highres 1girl...
[BASE FILE] (test_input.txt) Formatted tags saved to: C:\Users\admin\Documents\tag_formatter_test\test_input_formatted.txt
```

## Credits
- Me
- [@parabirb](https://github.com/parabirb) - Regex
- [@LuqueDaniel](https://github.com/LuqueDaniel) - pybooru
