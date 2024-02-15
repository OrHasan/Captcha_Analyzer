<a name="readme-top"></a>

<div align="center">
  <h2> Captcha_Analyzer </h2>
  <h5> Using a controlled Chrome browser, the code Browsing to the site, Capturing the captcha, Filtering all the noise from the text, Translating it to a text output, and finally Sending the result to the website </h5>
</div>

<br />

> [!NOTE]
> For now, this code is working only with "Zone-H" website, as other websites may use other captchas, and it also will require changes in the configurations file so the program will know where in the page each elemnt is located

<br />

<div align="center">
  
  ![Captcha Filtering Example][Filtering-Example]
  
</div>


<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
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
    <li><a href="#filters">Filters</a></li>
      <ul>
        <li><a href="#median-blur ">Median Blur</a></li>
        <li><a href="#erosion">Erosion</a></li>
        <li><a href="#dilation">Dilation</a></li>
      </ul>
  </ol>
</details>


<!-- CONFIGURATION FILE -->
## Configuration File
Almost any important data inside the code can be reconfigured directly from the `Analyzer Configurations.ini` file without the need to interact with the code itself.

In case of a missing file, the code will create it with the default data that can be found inside `def_config_file.py`. In case of a missing section or a specific key in one of the file sections, the code will replace the entire section with the default data (the rest of the file will be untouched).

**Analyzer Configurations.ini** - Detailed
```
[general]
data_folder = Data                                            # Data directory name
history_dir = %(data_folder)s/History                         # Directory of all captured captchas and the detection results for a future ML model
process_history_dir = %(history_dir)s/Filtering Process       # Filtering process pictures history
cleared_history_dir = %(history_dir)s/Cleared Captchas        # Final filtered pictures history
achieved_captcha_file = %(data_folder)s/New Captcha.png       # Where to save the current tested captcha
cleared_captcha_file = %(data_folder)s/Cleared Captcha.png    # Where to save the current filtered captcha
captcha_attempts = 20                                         # How many attempts to detect the captcha

[website]
website_url = https://www.zone-h.org/archive?hz=1            # The URL with the captcha
captcha_id = cryptogram                                      # html captcha ID
text_field_name = captcha                                    # html text field Name
submit_button_xpath = //*[@id='propdeface']/form/input[2]    # html submit button XPath

[filter]
use_median = True                    # Use the Median Blur filter on the captcha (good for salt-papper noise)
use_dilate_erode = False             # Use the Dilation & Erosion filters on the captcha (can used without the median or as addition to it)
median_kernel_size = 5               # Kernel/Mask size for the Median filter (use only odd numbers)
dilate_erode_kernel_size = (3, 3)    # Kernel/Mask size for the Dilation & Erosion filters
dilate_erode_iterations = 1          # How many iterations for each Dilation & Erosion filter

[client]
client_url = https://docparser-text-captcha-breaker.hf.space/    # The picture to text client URL
client_access_attempts = 3                                       # Client access attempts, in case of a timeout from the client in his response
client_access_delay = 0.25                                       # Delay between the access attempts to the client

[debug]
show_comparison = True    # Show the filtering process picture

[local_test]
test_type = Model Test                                      # Choice the test type:
                                                              # "Model Test" - Test the analysis model constancy
                                                              # "Filter Test" - Test different filtering steps
test_database_dir = ${general:data_folder}/Test Database    # Directory of all the desired captchas to run the test on
test_client_access_delay = 0.5                              # Same as "client_access_delay" but specific for the local test
model_test_repeats = 10                                     # How many times to run the Model Test on each captcha
methods_test_dir = ${general:data_folder}/Methods Test      # Directory to save the results of using different filtering steps
filter_1_dir = %(methods_test_dir)s/Filter 1                # Directory to save the results of using only the Median filter
filters_1_2_3_dir = %(methods_test_dir)s/Filters 1,2,3      # Directory to save the results of using all the filters together
filters_2_3_dir = %(methods_test_dir)s/Filters 2,3          # Directory to save the results of using only the Dilation & Erosion filters
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
- 1 step: Median filter
- 3 steps: Median filter -> Dilation filter -> Erosion filter
- 2 steps: Dilation filter -> Erosion filter

> [!NOTE]
> The Dilation & Erosion filters are in reversed order because the results they gave were inverted

<p align="right"><a href="#readme-top">back to top</a></p>


<!-- FILTERS -->
## Filters
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


<!-- MARKDOWN LINKS & IMAGES -->
[Filtering-Example]: Pictures/Captcha_Filtering_Example.png
[Median-Filter]: Pictures/Filters/Median_Filter.png
[Median-Filter-Example]: Pictures/Filters/Median_Filter_Example.png
[Erosion-Filter]: Pictures/Filters/Erosion_Filter.png
[Erosion-Filter-Example]: Pictures/Filters/Erosion_Filter_Example.png
[Dilation-Filter]: Pictures/Filters/Dilation_Filter.png
[Dilation-Filter-Example]: Pictures/Filters/Dilation_Filter_Example.png
