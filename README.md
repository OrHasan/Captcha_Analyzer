<a name="readme-top"></a>

<div align="center">
  <h2> Captcha_Analyzer </h2>
  <h5> Websites defacement data extraction project with a captcha solver that created after the 7.10, to help the OSINT process to detect attacks on Israeli websites as fast as possible and help cyber defence groups </h5>
  <h5> This happns by using a controlled Chrome browser: The code is Browsing to the site, Capturing the captcha, Filtering all the noise from the text in the picture, Translating it to a text output, and finally Sending the result to the website and starting to Extract the relevant data into SQL file </h5>
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
1.	Using Selenium, screenshot the captcha element
2.	Remove the frame & Filter the noise from the captcha with the selected method
3.	Send filtered picture to the API model ("Text Captcha Breaker")
4.	Correct the API results as to the specific captcha
5.	Send the result back to the site and check if passed
6.	Save the captcha, the filtered captcha and the filtering process with the pass/fail result in history folder for future ML improvements
7.	Redo the above steps if the site is asking for another captcha
(There are two consecutive captchas in case of running on "Zone-h" with a search filter, and more times in case of failing)
8.	Send the ZHE & PHPSESSID to the calling code, to able it to run without the captcha requirement
9.	Extract the relevant data from the website and save it into SQL DB


### Methods
14 different methods were tested simultaneously on 50 manually pre-solved captchas.
Thanks to this comparison, the best method was chosen as default, replacing a different one who once considered the best, and by that improving the single char detection by 13.6%, and the overall results by 26%.

<div align="center">

  ![Different Methods][Different-Methods]
  ![Methods Comparison][Methods-Comparison]
  ![Methods Detection Quality][Methods-Detection-Quality]
    
</div>


### API Correction
As it is known that the captcha in this website will never contain numbers or small letters, there is one additional step to reduce false detection by replacing such detection with similiar options (based on past false detections).
This step improved the results by 6-10%.

<div align="center">
  
  ![API-Correction][API-Correction]
  
</div>


<!-- CONFIGURATION FILE -->
## Configuration File
Almost any important data inside the code can be reconfigured directly from the `analyzer configurations.ini` file without the need to interact with the code itself.

In case of a missing file, the code will create it with the default data that can be found inside `def_config_file.py`. In case of a missing section or a specific key in one of the file sections, the code will replace the entire section with the default data (the rest of the file will be untouched).

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
**Test results constancy - Sending the cleared captcha _[model_test_repeats]_ times to the client**

For each captcha in the _[test_database_dir]_ folder there will be a progress bar, and in the end of each one all the results will be printed to the console with the result.


### Filter Test
**Test filters - Testing a different combination of the available filters**

Each file in the _[test_database_dir]_ folder need to be called with the expected result. The test will run each captcha with every specified filters combination in the code and save the filtering process picture in a corresponding sub-folder inside "Methods Test" folder.

The result files' names will be in the following logic:

`Captch #[Index] - '[Result]' ([X] of [Y] chars, [Z] extra chars).png`

Where:
- Index - Running index, according to the highest index currently in the folder
- Result - Client result from the filtered captcha
- X - How many correct chars were detected (same char in the same location as in the original file name)
- Y - How many chars available in the picture (according to the original file name)
- Z - How many extra chars were detected (`len(result) > Y`); if Z=0, this name section will be discarded

Testing the following filters combinations:
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
**(Use to clear _"Salt & Paper"_ noise)**

Running a mask on the picture (as example - 3x3), and replacing the pixel value in the center of the crossover between the picture and the mask with a middle value in the crossover (while looking on those values in ascending order).

<div align="center">
  
  ![Median Filter][Median-Filter]

  ![Median Filter - Example][Median-Filter-Example]
  
</div>

### Erosion
**(Use to shrink/remove objects)**

Running a mask on the picture, and removing any pixel that found in a place that the crossover between the picture and the mask aren't the same.

<div align="center">
  
  ![Erosion Filter][Erosion-Filter]

  ![Erosion Filter - Example][Erosion-Filter-Example]
  
</div>

### Dilation
**(Use to expand objects)**

Running a mask on the picture, and adding pixels in the crossover between the picture and the mask if the central pixel in the crossover is the same.

<div align="center">
  
  ![Dilation Filter][Dilation-Filter]

  ![Dilation Filter - Example][Dilation-Filter-Example]
  
</div>

<p align="right"><a href="#readme-top">back to top</a></p>


<!-- NOTES -->
## Notes
> [!NOTE]
> This code is working only with "Zone-H" website, as other websites may use other captchas that have not been reviewed. It is possible to add more options by improving the "website" key in the configurations file, so the program will know where in the page each elemnt is located


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
