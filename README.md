<a name="readme-top"></a>

<div align="center">
  <h2> Captcha_Analyzer </h2>
  <h5> This project was designed to extract data from defaced websites using a captcha solver. Created after the events of 7.10, it supports cyber defense groups by aiding the OSINT process in detecting attacks on Israeli websites as quickly as possible </h5>
  <h5> The program uses a controlled Chrome browser to browse the site, capture the captcha, filter out noise from the text in the image, translate it to text, send the result back to the site, and extract relevant data into an SQL file </h5>
</div>

<br />

<div align="center">
  
  ![Website Captcha][Website-Captcha]
  
</div>


<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#program-description">Program Description</a>
      <ul>
        <li><a href="#detailed-demonstration">Detailed Demonstration</a></li>
        <li><a href="#steps">Steps</a></li>
        <li><a href="#methods">Methods</a></li>
        <li><a href="#api-correction">API Correction</a></li>
      </ul>
    </li>
    <li>
      <a href="#configuration-file">Configuration File</a>
    </li>
    <li>
      <a href="#local-tester">Local Tester</a>
      <ul>
        <li><a href="#model-test">Model Test</a></li>
        <li><a href="#filter-test">Filter Test</a></li>
      </ul>
    </li>
    <li><a href="#filters-theory">Filters Theory</a></li>
      <ul>
        <li><a href="#median-blur ">Median Blur</a></li>
        <li><a href="#erosion">Erosion</a></li>
        <li><a href="#dilation">Dilation</a></li>
      </ul>
    <li>
      <a href="#notes">Notes</a>
    </li>
  </ol>
</details>


<!-- PROGRAM DESCRIPTION -->
## Program Description
### Detailed Demonstration
You can find a detailed video demonstration at:
https://drive.google.com/file/d/1A0nLMS7UPwGOVMGBurTfxIZb5HpDl4m0/view?usp=drive_link


### Steps
<div align="center">
  
  ![Program Steps][Program-Steps]
  
</div>

These are the steps the program follows:
1.	Use Selenium to screenshot the captcha element
2.	Remove the frame and filter the noise from the captcha using the selected method
3.	Send the filtered image to the API model ("Text Captcha Breaker")
4.	Correct the API results specific to the captcha
5.	Send the result back to the site and check if it passes
6.	Save the captcha, the filtered captcha, and the filtering process with the pass/fail result in the history folder for future ML improvements
7.	Repeat the above steps if the site requests another captcha (e.g. two consecutive captchas on "Zone-h" with a search filter, or more in case of failure)
8.	Send the ZHE & PHPSESSID cookies to the calling code to enable it to run without the captcha requirement
9.	Extract relevant data from the website and save it into an SQL database


### Methods
14 different methods were tested simultaneously on 50 manually pre-solved captchas.
Based on this comparison, the best method was chosen as the default, replacing the previously considered best method. This change improved single character detection by 13.6% and overall results by 26%.

<div align="center">

  ![Different Methods][Different-Methods]
  ![Methods Comparison][Methods-Comparison]
  ![Methods Detection Quality][Methods-Detection-Quality]
    
</div>


### API Correction
Since the captcha on this website never contains numbers or lowercase letters, an additional step was added to reduce false detections by replacing such detections with similar options based on past errors. This step improved results by 6-10%.

<div align="center">
  
  ![API-Correction][API-Correction]
  
</div>


<!-- CONFIGURATION FILE -->
## Configuration File
Almost all important data within the code can be reconfigured directly from the `analyzer configurations.ini` file without interacting with the code itself.

If the file is missing, the code will create it with default data found in `def_config_file.py`. If a section or specific key is missing in one of the file sections, the code will replace the entire section with default data, leaving the rest of the file untouched.

**analyzer configurations.ini** - Detailed
```
[general]
data_folder = data                                           # Data directory name
save_history = True                                          # Enable/Disable pictures save of captured captchas and the filtering process & results history (for a future ML model)
history_dir = ${data_folder}/history                         # Directory of all captured captchas and the filtering process & results (for a future ML model)
captcha_history_dir = ${history_dir}/captchas                # Original captchas pictures history
process_history_dir = ${history_dir}/filtering process       # Filtering process pictures history
cleared_history_dir = ${history_dir}/cleared captchas        # Final filtered pictures history
achieved_captcha_file = ${data_folder}/new captcha.png       # Where to save the current tested captcha
cleared_captcha_file = ${data_folder}/cleared captcha.png    # Where to save the current filtered captcha
captcha_attempts = 50                                        # How many attempts to detect the captcha
capcha_maximum_length = 5                                    # Maximum possible letters to take into account in the transcription result
letters_only = True                                          # Replace any number in the transcription result with similar letter
capitals_only = False                                        # Force capital letters - send the transcription result string with capitals only (it's important to take into account that "fix_similar_small_letters" has a higher priority and will occour first)
fix_similar_small_letters = True                             # Replace specific small letters in the transcription result string with similar capital letter (according to previous repeated detection mistakes)
selenium_minimum_wait = 1                                    # Declare minimum wait time for an element before throwing an error
selenium_condition_wait = 3                                  # Declare how much time to wait in case of a specific condition for an element

[website]
website_url = https://www.zone-h.org/archive/filter=1/published=0/domain=.il/fulltext=1/page=1?hz=1    # The URL with the captcha
captcha_id = cryptogram                                                                                # html captcha ID
text_field_css_selector = input[type='text']                                                           # html text field CSS selector
submit_button_css_selector = input[type='submit']                                                      # html submit button CSS selector
close_on_finish = False                                                                                # Close the driver (&browser) when the captcha transcription process is done
sql_file_name = IL10                                                                                   # The name of the SQL file where the extracted data from the website will be saved
pages_to_scan = 2                                                                                      # How many pages to scan from the website (as this is a fork version from my original code for 'Cyber7' for demonstration purpose only, the default value is 2 instead of 50 pages to save run time)

[filter]
use_median = False             # Use the Median Blur filter on the captcha (good for salt-papper noise)
use_median_mask = True         # after median filter, use the original picture as a mask to remove new pixels from originally empty spots (to avoid adding additional noise)
use_dilate_erode = True        # Use the Dilation & Erosion filters on the captcha (can used without the median or as addition to it)
median_kernel_size = 5         # Kernel/Mask size for the Median filter (use only odd numbers)
dilate_kernel_size = (3, 3)    # Kernel/Mask size for the Dilation filter
erode_kernel_size = (3, 3)     # Kernel/Mask size for the Erosion filter
dilate_iterations = 1          # How many iterations for each Dilation filter
erode_iterations = 1           # How many iterations for each Erosion filter

[client]
client_url = https://docparser-text-captcha-breaker.hf.space/    # The picture to text client URL
client_access_attempts = 3                                       # Client access attempts, in case of a timeout from the client in his response
client_access_delay = 0.25                                       # Delay between the access attempts to the client

[debug]
show_comparison = False    # Show the filtering process picture

[local_test]
test_type = Model Test                                                 # Choice the test type:
                                                                         # "Model Test" - Test the analysis model constancy
                                                                         # "Filter Test" - Test different filtering steps
test_database_dir = ${general:data_folder}/test database               # Directory of all the desired captchas to run the test on
test_client_access_delay = 0.5                                         # Same as "client_access_delay" but specific for the local test
model_test_repeats = 10                                                # How many times to run the Model Test on each captcha
methods_test_dir = ${general:data_folder}/methods test                 # Directory to save the results of using different filtering steps
filter_1_dir = ${methods_test_dir}/filter 1                            # Directory to save the results of using only the Median filter
filter_1_masked_dir = ${methods_test_dir}/filter 1 + mask              # Directory to save the results of using only the Median filter with mask
filters_1_2_3_dir = ${methods_test_dir}/filters 1,2,3                  # Directory to save the results of using all the filters together
filters_1_2_3_masked_dir = ${methods_test_dir}/filters 1,2,3 + mask    # Directory to save the results of using all the filters together with mask
filters_2_3_dir = ${methods_test_dir}/filters 2,3                      # Directory to save the results of using only the Dilation & Erosion filters
5_steps_filtering_dir = ${methods_test_dir}/5 steps filtering          # Directory to save the results of using 5 steps filtering process
6_steps_filtering_dir = ${methods_test_dir}/6 steps filtering          # Directory to save the results of using 6 steps filtering process
```

<p align="right"><a href="#readme-top">back to top</a></p>


<!-- LOCAL TESTER -->
## Local Tester
### Model Test
**The Model Test checks the consistency of test results by sending the cleared captcha _[model_test_repeats]_ times to the client**

For each captcha in the _[test_database_dir]_ folder, a progress bar will be displayed, and all results will be printed to the console at the end of each bar.


### Filter Test
**The Filter Test evaluates different combinations of available filters**

Each file in the _[test_database_dir]_ folder should be named with the expected result. The test runs each captcha with every specified filter combination and saves the filtering process images in corresponding sub-folders inside the 'Methods Test' folder.

The result files are named as follows:

`Captch #[Index] - '[Result]' ([X] of [Y] chars, [Z] extra chars).png`

Where:
- **Index**: Running index, according to the highest index currently in the folder
- **Result**: Client result from the filtered captcha
- **X**: Number of correct characters detected (same character in the same location as in the original file name)
- **Y**: Number of characters available in the picture (according to the original file name)
- **Z**: Number of extra characters detected (`len(result) > Y`); if Z=0, this section is discarded

Testing the following filter combinations:
```
- filter 1                  - 1 step:  Median filter
- filter 1 + mask           - 2 steps: Median filter -> Mask with original
- filters 1,2,3             - 3 steps: Median filter -> Dilation filter -> Erosion filter
- filters 1,2,3 + mask      - 4 steps: Median filter -> Mask with original -> Dilation filter -> Erosion filter
- filters 2,3               - 2 steps: Dilation filter -> Erosion filter
- 5 steps filtering + mask  - 6 steps: Median filter -> Mask with original -> Median filter -> Mask with original -> Enlarge by 300% -> Dilation filter
- 6 steps filtering + mask  - 7 steps: Median filter -> Mask with original -> Median filter -> Mask with original -> Enlarge by 300% -> Dilation filter -> Erosion filter
```

> [!NOTE]
> The Dilation & Erosion filters are in reversed order because the results they gave were inverted

<p align="right"><a href="#readme-top">back to top</a></p>


<!-- FILTERS THEORY -->
## Filters (theory)
### Median Blur
**Purpose: Clears _"Salt & Paper"_ noise**

**Method:** Applies a mask (e.g. 3x3) to the image and replaces the pixel value at the center of the mask with the median value of the pixels within the mask.

<div align="center">
  
  ![Median Filter][Median-Filter]

  ![Median Filter - Example][Median-Filter-Example]
  
</div>

### Erosion
**Purpose: Shrinks or removes objects**

**Method:** Applies a mask to the image and removes any pixel where the mask and the image do not match.

<div align="center">
  
  ![Erosion Filter][Erosion-Filter]

  ![Erosion Filter - Example][Erosion-Filter-Example]
  
</div>

### Dilation
**Purpose: Expands objects**

**Method:** Applies a mask to the image and adds pixels where the central pixel of the mask matches the image.

<div align="center">
  
  ![Dilation Filter][Dilation-Filter]

  ![Dilation Filter - Example][Dilation-Filter-Example]
  
</div>

<p align="right"><a href="#readme-top">back to top</a></p>


<!-- NOTES -->
## Notes
> [!NOTE]
> This code currently works only with the 'Zone-H' website, as other websites may use different captchas that have not been reviewed. It is possible to try other options by updating the 'website' section in the configurations file, allowing the program to locate each element on the page.


<!-- MARKDOWN LINKS & IMAGES -->
[Website-Captcha]: Pictures/Website_Captcha.png
[Different-Methods]: Pictures/Different_Methods.png
[Program-Steps]: Pictures/Program_Steps.png
[Methods-Comparison]: Pictures/Methods_Comparison.png
[Methods-Detection-Quality]: Pictures/Methods_Detection_Quality.png
[API-Correction]: Pictures/API_Correction.png
[Median-Filter]: Pictures/Filters/Median_Filter.png
[Median-Filter-Example]: Pictures/Filters/Median_Filter_Example.png
[Erosion-Filter]: Pictures/Filters/Erosion_Filter.png
[Erosion-Filter-Example]: Pictures/Filters/Erosion_Filter_Example.png
[Dilation-Filter]: Pictures/Filters/Dilation_Filter.png
[Dilation-Filter-Example]: Pictures/Filters/Dilation_Filter_Example.png
