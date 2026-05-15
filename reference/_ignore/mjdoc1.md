BELOW IS THE VERY ORIGINAL DOCUMENTATION. 



[
![Midjourney](//cdn.document360.io/logo/3040c2b6-fead-4744-a3a9-d56d621c6c7e/778d06e9a335497ba965629e3b83a31f-MJ_Boat.png)
](/)

  * [__](/v1/en)

Contents x

No matching results found

  * 

* * *

__ __

Tile

  *  __ Dark

 __ Light

 __Contents

# Tile

  *  __ Dark

 __ Light

* * *

Article summary

 __

Did you find this summary helpful? __ __ __ __

__

Thank you for your feedback

#### The `--tile` parameter generates images that can be used as repeating
tiles to create seamless patterns for fabrics, wallpapers and textures.

`--tile` works with [Model Versions](/models) `1` `2` `3` `test` `testp` `5`
`5.1` `5.2` and `6`.  
`--tile` only generates a single tile. Use a pattern making tool like this
[Seamless Pattern Checker ](//www.pycheung.com/checker/) to see the tile
repeat.

* * *

## Tile Examples

`prompt` `a pattern of pink and blue striped river stones --tile`  
![example of the motif image and tiled repeat created with the midjourney tile
parameter using model version 6 and the prompt a repeating pattern of pink and
blue striped river stones
--tile](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_tile_stripedStones.png)

  

`prompt` `a pattern of colorful watercolor fall leaves --tile`  
![example of the motif image and tiled repeat created with the midjourney tile
parameter using model version 6 and the prompt a pattern of colorful
watercolor fall leaves
--tile](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_tile_watercolorLeaves.png)

  

* * *

## How to Use the Tile Parameter

Add `--tile` to the end of your prompt.

![Animated Gif showing how the Midjourney tile parameter is
typed](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_Parameter_Tile.gif)

* * *

__

Previous

Next

 __

Table of contents

![Midjourney
Logo](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_LogoType.png)

Midjourney is an independent research lab exploring new mediums of thought and
expanding the imaginative powers of the human species. We are a small self-
funded team focused on design, human infrastructure, and AI.

FOLLOW US: [[F]](//www.facebook.com/groups/officialmidjourney)
[[T]](//twitter.com/midjourney) [[R]](//www.reddit.com/r/midjourney/)

Support

For questions or support visit the [ Midjourney Discord support
channels](//discord.com/channels/662267976984297473/958069758211797092/).

Sites

  * [Midjourney Website](//midjourney.com/)
  * [Midjourney Discord](//discord.gg/midjourney)

__

[
![Midjourney](//cdn.document360.io/logo/3040c2b6-fead-4744-a3a9-d56d621c6c7e/778d06e9a335497ba965629e3b83a31f-MJ_Boat.png)
](/)

  * [__](/v1/en)

Contents x

No matching results found

  * 

* * *

__ __

Aspect Ratios

  *  __ Dark

 __ Light

 __Contents

# Aspect Ratios

  *  __ Dark

 __ Light

* * *

Article summary

 __

Did you find this summary helpful? __ __ __ __

__

Thank you for your feedback

#### The `--ar` (or `--aspect`) parameter changes the aspect ratio of the
generated image. An aspect ratio is the width-to-height ratio of an image. It
is typically expressed as two numbers separated by a colon, such as 7:4 or
4:3.

A square image has equal width and height, described as a 1:1 aspect ratio.
The image could be 1000px × 1000px, or 1500px × 1500px, and the aspect ratio
would still be 1:1. A computer screen might have a ratio of 16:10. The width
is 1.6 times longer than the height. So the image could be 1600px × 1000px,
4000px × 2000px, 320px x 200px, etc.

  * The default aspect ratio is 1:1.
  * `--ar` must use whole numbers. Use 139:100 instead of 1.39:1.
  * The first number represents width, while the second number represents height. For portrait (tall) images, the second number should be larger. For landscape (wide) images, the first number should be larger.
  * The aspect ratio impacts the shape and composition of a generated image.
  * Some aspect ratios may be slightly changed when upscaling.
  * Older [Midjourney Version Models](/models) may not support all aspect ratios.

* * *

### Aspect Ratio Comparison

prompt example: `/imagine prompt` `vibrant California poppies --ar 5:4`

![Comparison of common Midjourney Aspect
Ratios](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_AspectRatioChart.png)

Extremely wide and tall aspect ratios are experimental and may produce
unpredictable results.

  

### Common Midjourney Aspect Ratios

`--ar 1:1` Default aspect ratio.  
`--ar 5:4` Common frame and print ratio.  
`--ar 3:2` Common in print photography.  
`--ar 7:4` Close to HD TV screens and smartphone screens.

  

* * *

## Changing the Aspect Ratio of an Image

Do you love an image you have generated but wish it was taller or wider? You
can use the Pan and Zoom features to adjust the aspect ratio of your images in
different ways. For more information, check out these pages:
[Pan](/v1/docs/pan-1), [Zoom](/v1/docs/zoom-out).

  

* * *

## How to Set the Aspect Ratio

### Use Aspect Ratio Parameters

Add `--aspect <value>:<value>`, or `--ar <value>:<value>` to the end of your
prompt on Discord or in the imagine bar on the website:

![Animated Gif showing how the Midjourney version parameter is
typed](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_Parameter_Aspect.gif)

  

### Website Settings

On the website, you can also set a default aspect ratio using the Settings
button in the imagine bar:

![](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/mj-
website-settings-aspect-ratio4.png)

  

The `Portrait` button will set your aspect ratio to 3:4. The `Landscape`
button will set it to 4:3. You can adjust the slider left for taller aspect
ratios, up to 1:2, or right for wider ones, up to 2:1.

The value you set here will apply to all your prompts unless you specify a
different value using the `--aspect` or `--ar` parameter in an individual
prompt.

Not all aspect ratios are supported by the slider, but you can use the `--ar`
parameter at the end of your prompt to set any ratio you'd like.

* * *

__

Previous

Next

 __

Table of contents

![Midjourney
Logo](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_LogoType.png)

Midjourney is an independent research lab exploring new mediums of thought and
expanding the imaginative powers of the human species. We are a small self-
funded team focused on design, human infrastructure, and AI.

FOLLOW US: [[F]](//www.facebook.com/groups/officialmidjourney)
[[T]](//twitter.com/midjourney) [[R]](//www.reddit.com/r/midjourney/)

Support

For questions or support visit the [ Midjourney Discord support
channels](//discord.com/channels/662267976984297473/958069758211797092/).

Sites

  * [Midjourney Website](//midjourney.com/)
  * [Midjourney Discord](//discord.gg/midjourney)

__

[
![Midjourney](//cdn.document360.io/logo/3040c2b6-fead-4744-a3a9-d56d621c6c7e/778d06e9a335497ba965629e3b83a31f-MJ_Boat.png)
](/)

  * [__](/v1/en)

Contents x

No matching results found

  * 

* * *

__ __

Repeat

  *  __ Dark

 __ Light

 __Contents

# Repeat

  *  __ Dark

 __ Light

* * *

Article summary

 __

Did you find this summary helpful? __ __ __ __

__

Thank you for your feedback

#### The `--repeat` or `--r` parameter runs a Job multiple times. Combine
`--repeat` with other parameters, like [\--chaos](/chaos) to increase the pace
of your visual exploration.

`--repeat` accepts values 2–4 for [Basic subscribers](/plans)  
`--repeat` accepts values 2–10 for [Standard subscribers](/plans)  
`--repeat` accepts values 2–40 for [Pro and Mega subscribers](/plans)  
The `--repeat` parameter can only be used in Fast and Turbo GPU mode.

  

* * *

### Use the `--repeat` or `--r` Parameter

Add `--repeat <value>` or `--r <value>` to the end of your prompt.

![animated gif showing how the midjourney repeat parameter is
typed](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_RepeatParameterGif.gif)

A **Job** is any action that uses the Midjourney Bot. **Jobs  **include using
`/imagine` to create an initial image grid, upscaling images, and creating
variations of images.

There are two modes for image generation, **Fast Mode** and**  Relax Mode**.
Fast Mode tries to give you a GPU instantly. It's the highest-priority
processing tier and uses your subscription's monthly GPU time. **Relax Mode**
queues your generation behind others based on how much you've used the system.
**Relax Mode** wait times are variable and usually range from 1-10 minutes.

By default, your images will be generated using **Fast** mode. You can switch
to **Relax  **if you have a Standard or Pro subscription.

* * *

__

Previous

Next

 __

![Midjourney
Logo](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_LogoType.png)

Midjourney is an independent research lab exploring new mediums of thought and
expanding the imaginative powers of the human species. We are a small self-
funded team focused on design, human infrastructure, and AI.

FOLLOW US: [[F]](//www.facebook.com/groups/officialmidjourney)
[[T]](//twitter.com/midjourney) [[R]](//www.reddit.com/r/midjourney/)

Support

For questions or support visit the [ Midjourney Discord support
channels](//discord.com/channels/662267976984297473/958069758211797092/).

Sites

  * [Midjourney Website](//midjourney.com/)
  * [Midjourney Discord](//discord.gg/midjourney)

__

[
![Midjourney](//cdn.document360.io/logo/3040c2b6-fead-4744-a3a9-d56d621c6c7e/778d06e9a335497ba965629e3b83a31f-MJ_Boat.png)
](/)

  * [__](/v1/en)

Contents x

No matching results found

  * 

* * *

__ __

No

  *  __ Dark

 __ Light

 __Contents

# No

  *  __ Dark

 __ Light

* * *

Article summary

 __

Did you find this summary helpful? __ __ __ __

__

Thank you for your feedback

#### The No parameter tells the Midjourney Bot what not to include in your
image.

`--no` accepts multiple words separated with commas: `--no item1, item2,
item3, item4`

  

### `--No` Comparison

`still life gouache painting`

![an image of a still life gouache painting made by midjourney using the
prompt still ife grouach
painting](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_NO_StillLife.jpg)

a range of objects appear in the still life

`still life gouache painting --no fruit`

![an image of a still life gouache painting made by midjourney using the
prompt still ife grouach painting --no
fruit](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_NO_StillLife_NoFruit.jpg)

The still life has fewer fruits

  

### `--no` vs. Don't

The Midjourney Bot considers every word in the prompt as a potential element
for the image. Prompting `still life gouache painting without any fruit` or
`still life gouache painting, please dont add fruit!` are _more_ likely to
produce pictures that include fruits because the relationship between
"without" or "don't" and the "fruit" is not interpreted by the Midjourney Bot
in the same way a human reader would understand it. To improve your results,
focus your prompt on what you do want to see in the image and use the "--no"
parameter to specify concepts you don't want to include.

`still life gouache painting`

![an image of a still life gouache painting made by midjourney using the
prompt still ife grouach
painting](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_NO_StillLife.jpg)

A range of objects appear in the still life.

`still life gouache painting, please don't add fruit!`

![an image of a still life gouache painting made by midjourney using the
prompt still ife grouach painting dont add
fruit](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_NO_StillLife_DONTFruit.jpg)

_More_ fruit is present in the final image.

  

## Multi Prompting

The `--no` parameter is the same as weighing part of a [multi prompt](/multi-
prompts) to "-.5" `still life gouache painting:: fruit::-.5` is the same as
`still life gouache painting --no fruit`.

  

* * *

## How to Use the No Paramter

Add `--no item1, item2, item3` to the end of your prompt.

![an animated gif showing how to type the Midjourney No
parameter](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_NoParameter.gif)

* * *

__

Previous

Next

 __

Table of contents

![Midjourney
Logo](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_LogoType.png)

Midjourney is an independent research lab exploring new mediums of thought and
expanding the imaginative powers of the human species. We are a small self-
funded team focused on design, human infrastructure, and AI.

FOLLOW US: [[F]](//www.facebook.com/groups/officialmidjourney)
[[T]](//twitter.com/midjourney) [[R]](//www.reddit.com/r/midjourney/)

Support

For questions or support visit the [ Midjourney Discord support
channels](//discord.com/channels/662267976984297473/958069758211797092/).

Sites

  * [Midjourney Website](//midjourney.com/)
  * [Midjourney Discord](//discord.gg/midjourney)

__

[
![Midjourney](//cdn.document360.io/logo/3040c2b6-fead-4744-a3a9-d56d621c6c7e/778d06e9a335497ba965629e3b83a31f-MJ_Boat.png)
](/)

  * [__](/v1/en)

Contents x

No matching results found

  * 

* * *

__ __

Style

  *  __ Dark

 __ Light

 __Contents

# Style

  *  __ Dark

 __ Light

* * *

Article summary

 __

Did you find this summary helpful? __ __ __ __

__

Thank you for your feedback

#### The `--style` parameter replaces the default aesthetic of some
[Midjourney Model Versions](/models).

Model Versions 6, 5.2, 5.1 and Niji 6 accept `--style raw`.

* * *

## The Effects of `--style raw`

`--style raw` uses an alternative model that may work well for users already
comfortable with prompting who want more control over their images. Images
made with `--style raw` have less automatic beautification applied, which can
result in a more accurate match when prompting for specific styles.

### Model Version 6

##### `--v 6`

![Midjourney Version v6 example image made using the prompt a black and white
oak tree
icon](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_Style_V6_Oak.jpg)

black and white oak tree icon

##### `--v 6 --style raw`

![Midjourney Version v6 example image made using the prompt a black and white
oak tree icon --style
raw](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_Style_V6_Oak_Raw.jpg)

black and white oak tree icon --style raw

  

##### `--v 6`

![Midjourney Version v6 example image made using the prompt a child's crayon
drawing of a
cat](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_Style_V6_ChildCat.jpg)

child's crayon drawing of a cat

##### `--v 6 --style raw`

![Midjourney Version v6 example image made using the prompt a child's crayon
drawing of a
cat](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_Style_V6_ChildCat_Raw.jpg)

child's crayon drawing of a cat --style raw

  

* * *

### Model Version 5.2

##### `--v 5.2`

![Midjourney Version v5.2 example image using prompt - ice cream icon
](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_Style_V52_IceCream.jpg)

ice cream icon

##### `--v 5.2 --style raw`

![Midjourney Version v5.2 example image using prompt - ice cream icon --style
raw](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_Style_V52_IceCReam_Raw.jpg)

ice cream icon --style raw

  

##### `--v 5.2 `

![Midjourney Version v5.2 example image using prompt - child drawing of a
cat](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_Style_V52_ChildCat.jpg)

child's drawing of a cat

##### `--v 5.2 --style raw`

![Midjourney Version v5.2 example image using prompt - child drawing of a cat
--style
raw](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_Style_V52_ChildCat_Raw.jpg)

child's drawing of a cat --style raw

  

* * *

## How to Use Styles

### Use the `--style` Parameter

Add `--style <style name>` to the end of your prompt on Discord or in the
imagine bar on the website:

![an animated gif showing how to type the midjourney --style
parameter](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_StyleParameter.gif)

  

### Use the Settings Command

Type `/settings` and select `🔧 RAW Mode` from the menu to append `--style raw`
to all prompts.

### Website Settings

You can choose between Standard and Raw styles as your default "Mode" with
buttons in the website Settings menu:

![](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/mj-
website-settings-raw.png)

  

Your current default style will be highlighted in red.

If `Standard Mode` is your default style, you can override it by adding
`--style raw` to individual prompts. If `Raw Mode` is your default, you'll
need to switch back to `Standard Mode` in your setings to turn it off.

* * *

__

Previous

Next

 __

Table of contents

![Midjourney
Logo](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_LogoType.png)

Midjourney is an independent research lab exploring new mediums of thought and
expanding the imaginative powers of the human species. We are a small self-
funded team focused on design, human infrastructure, and AI.

FOLLOW US: [[F]](//www.facebook.com/groups/officialmidjourney)
[[T]](//twitter.com/midjourney) [[R]](//www.reddit.com/r/midjourney/)

Support

For questions or support visit the [ Midjourney Discord support
channels](//discord.com/channels/662267976984297473/958069758211797092/).

Sites

  * [Midjourney Website](//midjourney.com/)
  * [Midjourney Discord](//discord.gg/midjourney)

__

[
![Midjourney](//cdn.document360.io/logo/3040c2b6-fead-4744-a3a9-d56d621c6c7e/778d06e9a335497ba965629e3b83a31f-MJ_Boat.png)
](/)

  * [__](/v1/en)

Contents x

No matching results found

  * 

* * *

__ __

Image Prompts

  *  __ Dark

 __ Light

 __Contents

# Image Prompts

  *  __ Dark

 __ Light

* * *

Article summary

 __

Did you find this summary helpful? __ __ __ __

__

Thank you for your feedback

#### You can use images as part of a prompt to influence a Job's composition,
style, and colors. Images prompts can be used alone or with text
prompts—experiment with combining images with different styles for the most
exciting results.

To add images to a prompt, type or paste the web address where the image is
stored online. The address must end in an extension like .png, .gif, or .jpg.
After adding image addresses, add any additional text and parameters to
complete the prompt.

![Image showing the Midjourney prompt
structure.](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ%20Prompt.png)

  

  * Prompts must have multiple image prompts or a single image prompt and a text prompt to work.
  * An image URL must be a direct link to an online image.
  * Your file should end in .png, .gif, .webp, .jpg, or .jpeg.
  * In most browsers, right-click or long-press an image and select Copy Image Address to get the URL.
  * The [`/blend` command](/blend) is a simplified image prompting process optimized for mobile users.
  * You can also use image URLs as [Style References](/v1/docs/style-reference) or [Character References](/v1/docs/character-reference).

  

Privacy Notes

  * Upload images in your direct messages with the Midjourney Bot to prevent other server users from seeing an image.
  * Image prompts and references are visible on the Midjourney website unless you're generating in [Stealth Mode](/v1/docs/stealth).

  

* * *

## How to Use an Image in Your Prompt

### 1\. Upload an image to Discord

[Follow these instructions to upload your image to
Discord.](//support.discord.com/hc/en-us/articles/211866427-How-do-I-upload-
images-and-GIFs)

  

### 2\. Copy your image's URL

*Discord Desktop App: Right-click on the image and select **Copy Link** (NOT "Copy Message Link").

  * Discord Web App: Click to expand the image, then right-click and choose "Copy image address."
  * Discord Mobile App: Tap and hold on the image, then select "Copy Media Link."

If none of these methods work, you can click to expand the image, and at the
bottom, select "Open in Browser" so you can copy and paste the image's URL.

To incorporate an image into your prompt, you need a direct image link that
ends with .png, .gif, .webp, .jpg, or .jpeg. If the image is on your computer
or phone, you can send it as a message to the Midjourney Bot first to generate
a link.

### How To Upload Your Image

## Add an Image URL to Your Prompt

To add an image to a prompt, begin typing `/imagine` as usual. After the
prompt box appears, drag the image file into the prompt box to add the image's
URL, or right-click and paste the link within the prompt box.

![Discord_FHZfwDLhLY.gif](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/Discord_FHZfwDLhLY.gif)

  

* * *

## Examples

### Starting Images

![Cropped image of a greecian statue generated with
Midjourney](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_ImagePrompt_Statue.png)

Greecian style statue

![Cropped image of vintage flower
illustraiton](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_ImagePrompt_Flowers.png)

Vintage Flower Illustration

![Cropped image of Ernst Haeckel's
Jellyfish](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_ImagePrompt_Jelly.jpg)

Ernst Haeckel's Jellyfish

![Cropped image of Ernst Haeckel's
Lichen](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_ImagePrompt_Lichen.png)

Ernst Haeckel's Lichen

![Cropped image of The Great Wave off
Kanagawa](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_ImagePrompt_Wave.png)

Hokusai's The Great Wave

  

### Midjourney Model Version 5

### Statue + Flowers

![Cropped image of the Bust of
Apollo](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_ImagePrompt_Statue.png)
\+ ![Cropped image of vintage flower
illustraiton](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_ImagePrompt_Flowers.png)

![Midjourney image prompt combining  a greecian style statue and a cropped
section of a vintage illustration of cyclamen
flowers](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_ImagePrompt_Statue_Flowers.jpg)

### Statue + Jellyfish

![Cropped image of the Bust of
Apollo](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_ImagePrompt_Statue.png)
\+ ![Cropped image of Ernst Haeckel's
Jellyfish](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_ImagePrompt_Jelly.jpg)
![Midjourney image prompt combining  a greecian style statue and a cropped
section of jellyfish by Ernst
Haeckel's](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_ImagePrompt_Statue_Jelly.jpg)

### Statue + Lichen

![Cropped image of the Bust of
Apollo](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_ImagePrompt_Statue.png)
\+ ![Cropped image of Ernst Haeckel's
Lichen](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_ImagePrompt_Lichen.png)
![Midjourney image prompt combining  a greecian style statue and a cropped
section of lichen by Ernst
Haeckel's](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_ImagePrompt_Statue_Lichen.jpg)

### Statue + Wave

![Cropped image of the Bust of
Apollo](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_ImagePrompt_Statue.png)
\+ ![Cropped image of The Great Wave off
Kanagawa](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_ImagePrompt_Wave.png)
![Midjourney image prompt combining  a greecian style statue and a cropped
section of the Great Wave off Kanagawa by
Hokusai](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_ImagePrompt_Statue_Wave.jpg)

### Statue + Lichen + Flowers

![Cropped image of the Bust of
Apollo](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_ImagePrompt_Statue.png)
\+ ![Cropped image of Ernst Haeckel's
Lichen](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_ImagePrompt_Lichen.png)
\+ ![Cropped image of vintage flower
illustraiton](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_ImagePrompt_Flowers.png)
![Midjourney image prompt combining  a greecian style statue, a cropped
section of lichen by Ernst Haeckel's, and a vintage floral
illustration](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_ImagePrompt_Statue_Flowers_Lichen.jpg)

  

Aspect Ratio Tip

Crop images to the same aspect ratio as your final image for the best results.

  

* * *

## Image Weight Parameter

Use the image weight parameter `--iw` to adjust the importance of the image
vs. text portion of a prompt. The default value is used when no `--iw` is
specified. Higher `--iw` values mean the image prompt will have more impact on
the finished job.

See the [Multi Prompts](/multi-prompts) page for more information about the
relative importance between parts of a prompt.

Different [Midjourney Version Models](/models) have different image weight
ranges.

| Version 6| Version 5| Version 4| niji 6| niji 5  
---|---|---|---|---|---  
Image Weight Default| 1| 1| NA| 1| 1  
Image Weight Range| 0–3| 0–2| NA| 0–3| 0–2  
  
  

prompt example: `/imagine prompt` `flowers.jpg birthday cake --iw .5`

![Cropped image of painter Jan Davidsz de Heem's Vase of Flowers used a
midjourney image
prompt](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/mj_iw-
start.jpg)

Image Prompt

![A midjourney image generated from an image prompt of an oil painting of
flowers and the prompt, a birthday cake with the image weight parameter set to
0.25](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/mj_iw-025.jpg)

\--iw .25

![A midjourney image generated from an image prompt of an oil painting of
flowers and the prompt, a birthday cake with the image weight parameter set to
0.5](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/mj_iw-050.jpg)

\--iw .5

![A midjourney image generated from an image prompt of an oil painting of
flowers and the prompt, a birthday cake with the image weight parameter set to
0.75](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/mj_iw-075.jpg)

\--iw .75

![A midjourney image generated from an image prompt of an oil painting of
flowers and the prompt, a birthday cake with the image weight parameter set to
1.0](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/mj_iw-100.jpg)

\--iw 1

![A midjourney image generated from an image prompt of an oil painting of
flowers and the prompt, a birthday cake with the image weight parameter set to
1.25](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/mj_iw-125.jpg)

\--iw 1.25

![A midjourney image generated from an image prompt of an oil painting of
flowers and the prompt, a birthday cake with the image weight parameter set to
1.5](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/mj_iw-150.jpg)

\--iw 1.5

![A midjourney image generated from an image prompt of an oil painting of
flowers and the prompt, a birthday cake with the image weight parameter set to
1.75](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/mj_iw-175.jpg)

\--iw 1.75

![A midjourney image generated from an image prompt of an oil painting of
flowers and the prompt, a birthday cake with the image weight parameter set to
2.0](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/mj_iw-200.jpg)

\--iw 2

![A midjourney image generated from an image prompt of an oil painting of
flowers and the prompt, a birthday cake with the image weight parameter set to
2.0](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/mj_iw-300.jpg)

\--iw 3

  

* * *

## Technical Details

Prompts that only use images and no text are not compatible with the
[\--stylize](/stylize), or [\--weird](/weird) parameters.

* * *

__

Previous

Next

 __

Table of contents

![Midjourney
Logo](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_LogoType.png)

Midjourney is an independent research lab exploring new mediums of thought and
expanding the imaginative powers of the human species. We are a small self-
funded team focused on design, human infrastructure, and AI.

FOLLOW US: [[F]](//www.facebook.com/groups/officialmidjourney)
[[T]](//twitter.com/midjourney) [[R]](//www.reddit.com/r/midjourney/)

Support

For questions or support visit the [ Midjourney Discord support
channels](//discord.com/channels/662267976984297473/958069758211797092/).

Sites

  * [Midjourney Website](//midjourney.com/)
  * [Midjourney Discord](//discord.gg/midjourney)

__

[
![Midjourney](//cdn.document360.io/logo/3040c2b6-fead-4744-a3a9-d56d621c6c7e/778d06e9a335497ba965629e3b83a31f-MJ_Boat.png)
](/)

  * [__](/v1/en)

Contents x

No matching results found

  * 

* * *

__ __

Seeds

  *  __ Dark

 __ Light

 __Contents

# Seeds

  *  __ Dark

 __ Light

* * *

Article summary

 __

Did you find this summary helpful? __ __ __ __

__

Thank you for your feedback

#### The Midjourney bot uses a seed number to create a field of visual noise,
like television static, as a starting point to generate the initial image
grids. Seed numbers are generated randomly for each image but can be specified
with the `--seed` parameter. If you use the same seed number and prompt, you
will get similar final images.

  * `--seed` accepts whole numbers 0–4294967295.
  * `--seed` values only influence the initial image grid.
  * Identical `--seed` values using [Model Versions](/models) `1`, `2`, `3`, `test`, and `testp` will produce images with similar composition, color, and details.
  * Identical `--seed` values using [Model Versions](/models) `4`, `5`, `6` and `niji` will produce nearly identical images.
  * Seed numbers are not static and should not be relied upon between sessions.

* * *

## Seed Parameter

If no Seed is specified, Midjourney will use a randomly generated seed number,
producing a wide variety of options each time a prompt is used.  
  

### Jobs run three times with random seeds:

prompt example: `/imagine prompt` `celadon owl pitcher`

![An example of an image grid made in midjourney V5.1 with a random
seed](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_SeedRandom_1.jpg)

![An example of an image grid made in midjourney V5.1 with a random
seed](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_SeedRandom_2.jpg)

![An example of an image grid made in midjourney V5.1 with a random
seed](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_SeedRandom_3.jpg)

  

### Jobs run three times with `--seed 12345`:

prompt example: `/imagine prompt` `celadon owl pitcher --seed 123`

![An example of an image grid made in midjourney with a seed of
12345](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_Seed123_1.jpg)

![An example of an image grid made in midjourney with a seed of
12345](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_Seed123_2.jpg)

![An example of an image grid made in midjourney with a seed of
12345](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_Seed123_3.jpg)

  

* * *

## How to Find a Job's Seed Number

### Use a Discord Emoji Reaction

Find the seed number of a Job in discord by [reacting with an ✉️ envelope
emoji](/discord-emoji-reactions) to a Job.

  

### Use The Show Command to Bring Back Old Jobs

To get the seed number for a past image, [copy the job ID ](show-job) and use
the `/show <Job ID #>` command with that ID to revive the Job. You can then
react to the newly regenerated Job with an ✉️ envelope emoji.

  

* * *

## How To Change Seed Numbers

### Use the `--seed` Parameter

Add `--seed <value>` to the end of your prompt.

![Animated Gif showing how the Midjourney Seed parameter is
typed](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_Seed_Gif.gif)

A **Job** is any action that uses the Midjourney Bot. **Jobs  **include using
`/imagine` to create an initial image grid, upscaling images, and creating
variations of images.

* * *

__

Previous

Next

 __

Table of contents

![Midjourney
Logo](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_LogoType.png)

Midjourney is an independent research lab exploring new mediums of thought and
expanding the imaginative powers of the human species. We are a small self-
funded team focused on design, human infrastructure, and AI.

FOLLOW US: [[F]](//www.facebook.com/groups/officialmidjourney)
[[T]](//twitter.com/midjourney) [[R]](//www.reddit.com/r/midjourney/)

Support

For questions or support visit the [ Midjourney Discord support
channels](//discord.com/channels/662267976984297473/958069758211797092/).

Sites

  * [Midjourney Website](//midjourney.com/)
  * [Midjourney Discord](//discord.gg/midjourney)

__

[
![Midjourney](//cdn.document360.io/logo/3040c2b6-fead-4744-a3a9-d56d621c6c7e/778d06e9a335497ba965629e3b83a31f-MJ_Boat.png)
](/)

  * [__](/v1/en)

Contents x

No matching results found

  * 

* * *

__ __

Weird

  *  __ Dark

 __ Light

 __Contents

# Weird

  *  __ Dark

 __ Light

* * *

Article summary

 __

Did you find this summary helpful? __ __ __ __

__

Thank you for your feedback

#### Explore unconventional aesthetics with the experimental `--weird` or
`--w` parameter. This parameter introduces quirky and offbeat qualities to
your generated images, resulting in unique and unexpected outcomes.

`--weird` accepts values: 0–3000.  
The default --weird value is 0.  
\--weird is a highly experimental feature. What's weird may change over time  
\--weird is compatible with [Midjourney Model Versions 5, 5.1, 5.2, 6, niji 5
and niji 6](/models)  
\--weird is not fully compatible with [seeds](/seeds)

* * *

## The Influence of Weird on Jobs

The optimal `--weird` value is dependent on the prompt and requires
experimentation. Try starting with smaller values, such as 250 or 500, and
then go up/down from there. If you want a generation to be conventionally
attractive and weird, try mixing higher `--stylize` values with `--weird`. Try
starting with similar values for both. Example `/imagine prompt` `cyanotype
cat --stylize 250 --weird 250`.

prompt example: `/imagine prompt` `cyanotype cat --weird 250`

##### `--weird 0`

![Example image generated using the Midjourney weird parameter, prompt:
cyanotype cat --weird
0](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_Weird_0.jpg)

##### `--weird 250`

![Example image generated using the Midjourney weird parameter, prompt:
cyanotype cat --weird
250](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_Weird_250.jpg)

##### `--weird 500`

![Example image generated using the Midjourney weird parameter, prompt:
cyanotype cat --weird
500](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_Weird_500.jpg)

##### `--weird 1000`

![Example image generated using the Midjourney weird parameter, prompt:
cyanotype cat --weird
1000](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_Weird_1000.jpg)

  

prompt example: `/imagine prompt` `lithograph potato --weird 250`

##### `--weird 0`

![Example image generated using the Midjourney weird parameter, prompt:
lithograph potato --weird
0](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_Weird_Potato_0.jpg)

##### `--weird 250`

![Example image generated using the Midjourney weird parameter, prompt:
lithograph potato --weird
250](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_Weird_Potato_250.jpg)

##### `--weird 500`

![Example image generated using the Midjourney weird parameter, prompt:
lithograph potato --weird
500](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_Weird_Potato_500.jpg)

##### `--weird 1000`

![Example image generated using the Midjourney weird parameter, prompt:
lithograph potato --weird
1000](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_Weird_Potato_1000.jpg)

  

prompt example: `/imagine prompt` `clockwork chicken --weird 250`

##### `--weird 0`

![Example image generated using the Midjourney weird parameter, prompt:
lithograph potato --weird
0](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_Weird_Chicken_0.jpg)

##### `--weird 250`

![Example image generated using the Midjourney weird parameter, prompt:
lithograph potato --weird
250](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_Weird_Chicken_250.jpg)

##### `--weird 500`

![Example image generated using the Midjourney weird parameter, prompt:
lithograph potato --weird
500](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_Weird_Chicken_500.jpg)

##### `--weird 1000`

![Example image generated using the Midjourney weird parameter, prompt:
lithograph potato --weird
1000](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_Weird_Chicken_1000.jpg)

  

* * *

## What's the difference between `--weird`, `--chaos`, and `--stylize`?

`--chaos` controls how diverse the initial grid images are from each other.  
`--stylize` controls how strongly Midjourney's default aesthetic is applied.  
`--weird` controls how unusual an image is compared to previous Midjourney
images.

  

* * *

## How to Use Weird

### Use the Weird Parameter

Add `--weird <value>` or `--w <value>` to the end of your prompt on Discord or
in the imagine bar on the website:

![Animated Gif showing how the Midjourney version weird is
typed](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/WeirdParamter.gif)

### Website Settings

You can set a default Weirdness using the Settings button in the imagine bar:

![](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/mj-
website-settings-weird.png)

  

Adjust the slider left for lower values and right for higher values.

The value you set here will apply to all your prompts unless you specify a
different value using the `--weird` or `--w` parameter in an individual
prompt.

* * *

__

Previous

Next

 __

![Midjourney
Logo](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_LogoType.png)

Midjourney is an independent research lab exploring new mediums of thought and
expanding the imaginative powers of the human species. We are a small self-
funded team focused on design, human infrastructure, and AI.

FOLLOW US: [[F]](//www.facebook.com/groups/officialmidjourney)
[[T]](//twitter.com/midjourney) [[R]](//www.reddit.com/r/midjourney/)

Support

For questions or support visit the [ Midjourney Discord support
channels](//discord.com/channels/662267976984297473/958069758211797092/).

Sites

  * [Midjourney Website](//midjourney.com/)
  * [Midjourney Discord](//discord.gg/midjourney)

__

[
![Midjourney](//cdn.document360.io/logo/3040c2b6-fead-4744-a3a9-d56d621c6c7e/778d06e9a335497ba965629e3b83a31f-MJ_Boat.png)
](/)

  * [__](/v1/en)

Contents x

No matching results found

  * 

* * *

__ __

Stylize

  *  __ Dark

 __ Light

 __Contents

# Stylize

  *  __ Dark

 __ Light

* * *

Article summary

 __

Did you find this summary helpful? __ __ __ __

__

Thank you for your feedback

#### The Midjourney Bot has been trained to produce images that favor artistic
color, composition, and forms. The `--stylize` or `--s` parameter influences
how strongly this training is applied. Low stylization values produce images
that closely match the prompt but are less artistic. High stylization values
create images that are very artistic but less connected to the prompt.

`--stylize`'s default value is 100 and accepts integer values 0–1000 when
using the [current models](/models)

  

* * *

## Common Stylize Settings

### Influence of Stylize on Model Version 6

prompt example: `/imagine prompt` `child's drawing of a cat --s 100`

##### `--stylize 0`

![Midjourney style parameter example. Image of the prompt childs drawing of a
cat
stylize=0](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_Stylize_ChildsCat_0.jpg)

##### `--stylize 50`

![Midjourney style parameter example. Image of the prompt childs drawing of a
cat
stylize=0](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_Stylize_ChildsCat_50.jpg)
Equal to `🖌️ Style Low`

##### `--stylize 100` (default)

![Midjourney style parameter example. Image of the prompt childs drawing of a
cat
stylize=100](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_Stylize_ChildsCat_100.jpg)
Equal to `🖌️ Style Med`

  

##### `--stylize 250`

![Midjourney style parameter example. Image of the prompt childs drawing of a
cat
stylize=250](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_Stylize_ChildsCat_250.jpg)
Equal to `🖌️ Style High`

##### `--stylize 500`

![Midjourney style parameter example. Image of the prompt childs drawing of a
cat
stylize=500](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_Stylize_ChildsCat_500.jpg)

##### `--stylize 750`

![Midjourney style parameter example. Image of the prompt childs drawing of a
cat
stylize=750](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_Stylize_ChildsCat_750.jpg)
Equal to `🖌️ Style Very High`

  
  
  

prompt example: `/imagine prompt` `colorful risograph of a fig --s 100`

`--stylize 50`

![Midjourney style parameter example. Image of the prompt colorful risograph
of a fig
stylize=50](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_Stylize_Fig50.jpg)
Equal to `🖌️ Style Low`

`--stylize 100` (default)

![Midjourney style parameter example. Image of the prompt colorful risograph
of a fig
stylize=100](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_Stylize_Fig100.jpg)
Equal to `🖌️ Style Med`

`--stylize 250`

![Midjourney style parameter example. Image of the prompt colorful risograph
of a fig
stylize=250](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_Stylize_Fig250.jpg)
Equal to `🖌️ Style High`

`--stylize 750`

![Midjourney style parameter example. Image of the prompt colorful risograph
of a fig
stylize=750](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_Stylize_Fig750.jpg)
Equal to `🖌️ Style Very High`

  

* * *

## How to Use Stylize

### Use the Stylize Parameter

Add `--stylize <value>` or `--s <value>` to the end of your prompt on Discord
or in the imagine bar on the website:

![Image showing how to use the Midjourney style
parameter.](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/imagine-
prompt-stylize.png)

  

### Use the Discord Settings Command

Type `/settings` and select your preferred stylize value from the menu.

`🖌️ Style Low` `🖌️ Style Med` `🖌️ Style High` `🖌️ Style Very High`

### Website Settings

You can set a default Stylization using the Settings button in the imagine
bar:

![](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/mj-
website-settings-stylize.png)

  

Adjust the slider left for lower values and right for higher values.

The value you set here will apply to all your prompts unless you specify a
different value using the `--stylize` or `--s` parameter in an individual
prompt.

* * *

__

Previous

Next

 __

Table of contents

![Midjourney
Logo](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_LogoType.png)

Midjourney is an independent research lab exploring new mediums of thought and
expanding the imaginative powers of the human species. We are a small self-
funded team focused on design, human infrastructure, and AI.

FOLLOW US: [[F]](//www.facebook.com/groups/officialmidjourney)
[[T]](//twitter.com/midjourney) [[R]](//www.reddit.com/r/midjourney/)

Support

For questions or support visit the [ Midjourney Discord support
channels](//discord.com/channels/662267976984297473/958069758211797092/).

Sites

  * [Midjourney Website](//midjourney.com/)
  * [Midjourney Discord](//discord.gg/midjourney)

__

[
![Midjourney](//cdn.document360.io/logo/3040c2b6-fead-4744-a3a9-d56d621c6c7e/778d06e9a335497ba965629e3b83a31f-MJ_Boat.png)
](/)

  * [__](/v1/en)

Contents x

No matching results found

  * 

* * *

__ __

Model Version 4

  *  __ Dark

 __ Light

 __Contents

# Model Version 4

  *  __ Dark

 __ Light

* * *

Article summary

 __

Did you find this summary helpful? __ __ __ __

__

Thank you for your feedback

#### Midjourney regularly introduces new model versions to improve coherency,
efficiency, quality, and style. You can switch model versions by using the
[/settings](/settings-and-presets) command and selecting your preferred model
version. Different models excel at producing different types of images.

#### [Read about the latest Midjourney Models here](/models)

* * *

### Default Paramter Values

Model Version 4

| Aspect Ratio| Chaos| Quality| Seed| Stop| Style| Stylize  
---|---|---|---|---|---|---|---  
Default Value  
| 1:1| 0| 1| Random| 100| 4c| 100  
Range  
| 1:2–2:1| 0–100| .25 .5 or 1| whole numbers 0–4294967295| 10–100| 4a, 4b, or
4c| 0–1000  
  
  

* * *

## Model Version 4 (Legacy)

The Midjourney V4 model is an entirely new codebase and brand-new AI
architecture designed by Midjourney and trained on the new Midjourney AI
supercluster. The latest Midjourney model has more knowledge of creatures,
places, objects, and more. It's much better at getting small details right and
can handle complex prompts with multiple characters or objects. The Version 4
model supports advanced functionality like image prompting and multi-prompts.

This model has very high Coherency and excels with [Image Prompts](/image-
prompts).

  

![Midjourney Version 4 example image of the prompt Vibrant California
Poppies](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_V4_Poppies.png)

Prompt: vibrant California poppies

![](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/high_contrast.png)

Prompt: high contrast surreal collage

  

### Version 4 Styles 4a, 4b, and 4c

Midjourney Model Version 4 has three slightly different "flavors" with slight
tweaks to the stylistic tuning of the model. Experiment with these versions by
adding `--style 4a`, `--style 4b`, or `--style 4c` to the end of a V4 prompt.

`--v 4 --style 4c` is the current default and does not need to be added to the
end of a prompt.

Note on Style 4a and 4b

`--style 4a` and `--style 4b` only support 1:1, 2:3, and 3:2 aspect ratios.  
`--style 4c` support aspect ratios up to 1:2 or 2:1.

##### `--style 4a`

![Midjourney Version 4a example
image](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_V4a.jpg)

vibrant California poppies --style 4a

##### `--style 4b`

![Midjourney Version 4b example
image](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_V4b.jpg)

vibrant California poppies --style 4b

##### `--style 4c`

![Midjourney Version 4c example
image](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_4c.png)

vibrant California poppies --style 4c

##### `--style 4a`

![Midjourney Version 4a example
image](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_V4a_fish.jpg)

school of fish --style 4a

##### `--style 4b`

![Midjourney Version 4b example
image](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_V4b_fish.jpg)

school of fish --style 4b

##### `--style 4c`

![Midjourney Version 4c example
image](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_4c_fish.png)

school of fish --style 4c

  

* * *

## Niji Model 4 (Legacy)

The `niji 4` model is a collaboration between Midjourney and
[Spellbrush](//spellbrush.com/) tuned to produce anime and illustrative
styles. The `--niji 4` model has vastly more knowledge of anime, anime styles,
and anime aesthetics. It's excellent at dynamic and action shots and
character-focused compositions in general.

prompt example: `/imagine prompt` `vibrant California poppies --niji 4`

##### `--v 4`

![Midjourney Version v4 example image of the prompt vibrant california
poppies](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_4c.png)

California poppies --v 4

##### `--niji 4`

![Midjourney Version niji example image of the
prompt](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_Niji.jpg)

California poppies --niji 4

##### `--v 4`

![Midjourney Version v4 example image of the prompt vibrant california
poppies](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_V4_birdTwig.jpg)

birds sitting on a twig --v 4

##### `--niji 4`

![Image of Midjourney niji model using the prompt birds sitting on a
twig](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_Niji_birdTwig.jpg)

birds sitting on a twig --niji 4

  

* * *

## V4 Upscaler Tools

Earlier Midjourney model versions start by generating a grid of low-resolution
image options for each Job. You can use a Midjourney upscaler on any of these
images to increase the size and add additional details. There are multiple
upscale models available for upscaling an image. Using an upscaler uses your
subscription's GPU minutes.

The `U1` `U2` `U3` `U4` buttons under each image grid are used to upscale the
selected image.

[Read more about current upscaling options](/upscalers)

  

### Midjourney Dimensions and Sizes

 _All sizes are for square 1:1 aspect ratios._

Model Version| Starting Grid Size| V4 Default Upscaler| Detail Upscale| Light
Upscale| Beta Upscale  
---|---|---|---|---|---  
Version 4| 512 x 512| 1024 x 1024| 1024 x 1024| 1024 x 1024| 2048 x 2048  
niji 4| 512 x 512| 1024 x 1024| 1024 x 1024| 1024 x 1024| 2048 x 2048  
  
### Model Version 4 Upscaler

The Midjourney Model Version 4 upscaler increases image size while smoothing
or refining details. Some small elements may change between the initial grid
image and the finished upscale.

##### prompt: `adorable rubber duck medieval knight`

![](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_Upscaler_Regular.png)

##### prompt: `sand cathedral`

![](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_Upscaler_Regular2.png)

* * *

## Influence of [Stylize](/stylize) on Model V4

prompt example: `/imagine prompt` `illustrated figs --v 4 --s 100`

`--stylize 50`

![Midjourney style parameter example. Image of the prompt illustrated figs
with
style=50](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_Stylize_0.jpg)

`🖌️ Style Low`

`--stylize 100` (default)

![Midjourney stylize parameter example. Image of the prompt illustrated figs
with
style=100](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_Stylize_100.jpg)

`🖌️ Style Med`

`--stylize 250`

![Midjourney stylize parameter example. Image of the prompt illustrated figs
with
style=250](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_Stylize_250.jpg)

`🖌️ Style High`

`--stylize 750`

![Midjourney stylize parameter example. Image of the prompt illustrated figs
with
style=750](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_Stylize_750.jpg)

`🖌️ Style Very High`

  

* * *

**Coherency** is the strength of the connection between the text prompt and
the resulting image. A high degree of coherency means that the image will be
an accurate representation of the prompt text.

The Midjourney Bot processes jobs on high-end GPUs. Each minute that it takes
to complete a job is a **GPU minute**. You have a limited amount of GPU
minutes when in **Fast Mode**. Because image generations may be processed on
multiple GPUs simultaneously, GPU minutes are not directly connected to the
time you wait for an image to generate.

* * *

__

Previous

Next

 __

Table of contents

![Midjourney
Logo](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_LogoType.png)

Midjourney is an independent research lab exploring new mediums of thought and
expanding the imaginative powers of the human species. We are a small self-
funded team focused on design, human infrastructure, and AI.

FOLLOW US: [[F]](//www.facebook.com/groups/officialmidjourney)
[[T]](//twitter.com/midjourney) [[R]](//www.reddit.com/r/midjourney/)

Support

For questions or support visit the [ Midjourney Discord support
channels](//discord.com/channels/662267976984297473/958069758211797092/).

Sites

  * [Midjourney Website](//midjourney.com/)
  * [Midjourney Discord](//discord.gg/midjourney)

__

[
![Midjourney](//cdn.document360.io/logo/3040c2b6-fead-4744-a3a9-d56d621c6c7e/778d06e9a335497ba965629e3b83a31f-MJ_Boat.png)
](/)

  * [__](/v1/en)

Contents x

No matching results found

  * 

* * *

__ __

Multi Prompts

  *  __ Dark

 __ Light

 __Contents

# Multi Prompts

  *  __ Dark

 __ Light

* * *

Article summary

 __

Did you find this summary helpful? __ __ __ __

__

Thank you for your feedback

#### The Midjourney Bot can blend multiple concepts using :: as a separator.
Using a multi-prompt allows you to assign relative importance to the concept
in the prompt, helping you control how they are blended together.

## Multi-Prompt Basics

Adding a double colon `::` to a prompt indicates to the Midjourney Bot that it
should consider each part of the prompt individually. For the prompt `space
ship` both words are considered together, and the Midjourney Bot produces
images of sci-fi spaceships. If the prompt is separated into two parts,
`space:: ship`, both concepts are considered separately, then blended together
creating a sailing ship traveling through space.  
  

There is no space between the double colons `::`  
Multi-prompts work with [Model Versions](/models) `1`, `2`, `3`, `4`, `'5`,
`niji`, and `niji 5`  
Any [parameters](/parameter-list) are still added to the very end of the
prompt.

  

### `space ship`

![Image of the Midjourney Prompt space
ship](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/Midjourney_MultiPrompt_Space-
Ship.jpg)

 _space ship_ is considered as a single thought.

### `space:: ship`

![Image of the Midjourney Prompt space::1
ship](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/Midjourney_MultiPrompt_Space1_Ship1.jpg)

 _space_ and _ship_ are considered separate thoughts

`cheese cake painting`

![Image of the Midjourney Prompt cheese cake
painting](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/Midjourney_MultiPrompt_Cheese_Cake_Painting.jpg)

 _cheese cake painting_ is considered together, producing a painted image of a
cheesecake.

`cheese:: cake painting`

![Image of the Midjourney Prompt cheese:: cake
painting](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/Midjourney_MultiPrompt_Cheese1_Cake_Painting.jpg)

 _cheese_ is considered separately from _cake painting_ , producing images of
painted cakes made of cheeses.

`cheese:: cake:: painting`

![Image of the Midjourney Prompt cheese:: cake::
painting](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/Midjourney_MultiPrompt_Cheese1_Cake1_Painting1.jpg)

 _cheese_ , _cake_ , and _painting_ are considered separately, producing
tiered cakes, made of cheeses with common classical painting compositions and
elements.

## Prompt Weights

When a double colon `::` is used to separate a prompt into different parts,
you can add a number immediately after the double colon to assign the relative
importance to that part of the prompt.

In the example below, the prompt `space:: ship` produced a sailing ship
traveling through space. Changing the prompt to `space::2 ship` makes the word
**space** twice as important as the word ship, producing images of space that
have ships as a supporting element.

[Model Versions] `1`, `2`, `3` only accept whole numbers as weights  
[Model Versions] `4`, `niji 4`, `niji 5`, `5`, `5.1`, and `5.2` and can accept
decimal places for weights  
Non-specified weights default to 1.

### `space:: ship`

![Image of the Midjourney Prompt space::1
ship](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/Midjourney_MultiPrompt_Space1_Ship1.jpg)

 _space_ and _ship_ are considered as separate thoughts

### `space::2 ship`

![Image of the Midjourney Prompt space
ship](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/Midjourney_MultiPrompt_Space2_Ship1.jpg)

 _space_ is twice as important as _ship_

**Weights are normalized:**  
`space:: ship` is the same as `space::1 ship`, `space:: ship::1`,`space::2
ship::2`, `space::100 ship::100`, etc.  
`cheese::2 cake` is the same as `cheese::4 cake::2`, `cheese::100 cake::50`
etc.  
`cheese:: cake:: painting` is the same as `cheese::1 cake::1 painting::1`,
`cheese::1 cake:: painting::`, `cheese::2 cake::2 painting::2` etc.

  

* * *

### Negative Prompt Weights

Negative weights can be added to parts of a multi-prompt to help remove
unwanted elements.  
The sum of all weights must be a positive number.

`still life gouache painting`

![an image of a still life gouache painting made by midjourney using the
prompt still ife grouach
painting](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_NO_StillLife.jpg)

a range of objects appear in the still life

`still life gouache painting:: fruit::-.5`

![an image of a still life gouache painting made by midjourney using the
prompt still ife grouach painting --no
fruit](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_NO_StillLife_NoFruit.jpg)

The still life has fewer fruits

  

### The `--no` Parameter

The `--no` [parameter](/no) is the same as weighing part of a multi prompt to
"-.5" `vibrant tulip fields:: red::-.5` is the same as `vibrant tulip fields
--no red`.

  

* * *

__

Previous

Next

 __

Table of contents

![Midjourney
Logo](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_LogoType.png)

Midjourney is an independent research lab exploring new mediums of thought and
expanding the imaginative powers of the human species. We are a small self-
funded team focused on design, human infrastructure, and AI.

FOLLOW US: [[F]](//www.facebook.com/groups/officialmidjourney)
[[T]](//twitter.com/midjourney) [[R]](//www.reddit.com/r/midjourney/)

Support

For questions or support visit the [ Midjourney Discord support
channels](//discord.com/channels/662267976984297473/958069758211797092/).

Sites

  * [Midjourney Website](//midjourney.com/)
  * [Midjourney Discord](//discord.gg/midjourney)

__

[
![Midjourney](//cdn.document360.io/logo/3040c2b6-fead-4744-a3a9-d56d621c6c7e/778d06e9a335497ba965629e3b83a31f-MJ_Boat.png)
](/)

  * [__](/v1/en)

Contents x

No matching results found

  * 

* * *

__ __

Permutation Prompts

  *  __ Dark

 __ Light

 __Contents

# Permutation Prompts

  *  __ Dark

 __ Light

* * *

Article summary

 __

Did you find this summary helpful? __ __ __ __

__

Thank you for your feedback

#### Permutation Prompts allow you to quickly generate variations of a prompt
with a single `/imagine` command. By including lists of options separated with
commas `,` within curly braces `{}` in your prompt, you can create multiple
versions of a prompt with different combinations of those options.

[Basic Subscribers](/plans) can create a maximum of 4 Jobs with a single
Permutation Prompt.  
[Standard Subscribers](/plans) can create a maximum of 10 Jobs with a single
Permutation Prompt.  
[Pro and Mega Subscribers](/plans) can create a maximum of 40 Jobs with a
single Permutation Prompt.

You can use Permutation Prompts to create combinations and permutations
involving any part of a Midjourney Prompt, including text, [image
prompts](/image-prompts), [parameters](/parameter-list), or [prompt
weights](/multi-prompts).  
Permutation prompts are only available while using Fast mode.

* * *

## Permutation Prompt Basics

Separate your list of options within curly brackets {} to quickly create and
process multiple prompt variations.  
  

**Prompt Example:**  
`/imagine prompt` `a {red, green, yellow} bird` creates and processes three
Jobs.

`/imagine prompt` `a red bird`  
`/imagine prompt` `a green bird`  
`/imagine prompt` `a yellow bird`

  

GPU Minutes

The Midjourney Bot processes each Permutation Prompt variation as an
individual Job. Each Job consumes GPU minutes.

Permutation Prompts will show a confirmation message before they begin
processing.

  

* * *

## Permutation Prompt Examples

### Prompt Text Variations

The prompt `/imagine prompt` `a naturalist illustration of a {pineapple,
blueberry, rambutan, banana} bird` will create and process four Jobs:

![A midjourney generated image of a a pineapple
bird](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_Combo_pineappleBird.jpg)

a naturalist illustration of a pineapple bird

![A midjourney generated image of a blueberry
bird](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_Combo_blueberryBird.jpg)

a naturalist illustration of a blueberry bird

![A midjourney generated image of a rambutan
bird](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_Combo_rambutanBird.jpg)

a naturalist illustration of a rambutan bird

![A midjourney generated image of a banana
bird](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_Combo_bananaBird.jpg)

a naturalist illustration of a banana bird

  

* * *

### Prompt Parameter Variations

The prompt `/imagine prompt` `a naturalist illustration of a fruit salad bird
--ar {3:2, 1:1, 2:3, 1:2}` will create and process four Jobs with different
[aspect ratios](/aspect-ratios):

![A midjourney generated image of a fruit salad bird with a 3:2 aspect
ratio](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_combo_AR32.jpg)

a naturalist illustration of a fruit salad bird --ar 3:2

![A midjourney generated image of a fruit salad bird with a 1:1 aspect
ratio](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_combo_AR11.png)

a naturalist illustration of a fruit salad bird --ar 1:1

![A midjourney generated image of a fruit salad bird with a 2:3 aspect
ratio](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_combo_AR23.jpg)

a naturalist illustration of a fruit salad bird --ar 2:3

![A midjourney generated image of a fruit salad bird with a 1:1 aspect
ratio](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_combo_AR12.jpg)

a naturalist illustration of a fruit salad bird --ar 1:2

  

The prompt `/imagine prompt` `a naturalist illustration of a fruit salad bird
--{v 5, niji, test}` will create and process three Jobs using different
Midjourney [Model Versions](/models):

![A midjourney generated image of a fruit salad bird using the v5
model](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_Combo_v5.jpg)

a naturalist illustration of a fruit salad bird --v 5

![A midjourney generated image of a fruit salad bird using the niji
model](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_Combo_niji.jpg)

a naturalist illustration of a fruit salad bird --niji

![A midjourney generated image of a fruit salad bird using the test
model](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_Combo_test.jpg)

a naturalist illustration of a fruit salad bird --test

  

* * *

### Multiple and Nested Permutations

It is possible to use multiple sets of bracketed options in a single prompt.  
`/imagine prompt` `a {red, green} bird in the {jungle, desert}` creates and
processes four Jobs.

`/imagine prompt` `a red bird in the jungle`  
`/imagine prompt` `a red bird in the desert`  
`/imagine prompt` `a green bird in the jungle`  
`/imagine prompt` `a green bird in the desert`

  

It is also possible to nest sets of bracketed options inside other sets of
brackets within a single prompt:

Example: `/imagine prompt` `A {sculpture, painting} of a {seagull {on a pier,
on a beach}, poodle {on a sofa, in a truck}}.`

`/imagine prompt` `A sculpture of a seagull on a pier.`  
`/imagine prompt` `A sculpture of a seagull on a beach.`  
`/imagine prompt` `A sculpture of a poodle on a sofa.`  
`/imagine prompt` `A sculpture of a poodle in a truck.`  
`/imagine prompt` `A painting of a seagull on a pier.`  
`/imagine prompt` `A painting of a seagull on a beach.`  
`/imagine prompt` `A painting of a poodle on a sofa.`  
`/imagine prompt` `A painting of a poodle in a truck.`  
  

* * *

### Escape Character

If you want to include a `,` within the curly brackets that does not act as a
separator place a backslash `\` directly before it.

`imagine prompt` `{red, pastel, yellow} bird` produces three Jobs  
`/imagine prompt` `a red bird`  
`/imagine prompt` `a pastel bird`  
`/imagine prompt` `a yellow bird`

`imagine prompt` `{red, pastel \, yellow} bird` produces two Jobs  
`/imagine prompt` `a red bird`  
`/imagine prompt` `a pastel, yellow bird`

There are two modes for image generation, **Fast Mode** and**  Relax Mode**.
Fast Mode tries to give you a GPU instantly. It's the highest-priority
processing tier and uses your subscription's monthly GPU time. **Relax Mode**
queues your generation behind others based on how much you've used the system.
**Relax Mode** wait times are variable and usually range from 1-10 minutes.

By default, your images will be generated using **Fast** mode. You can switch
to **Relax  **if you have a Standard or Pro subscription.

A **Job** is any action that uses the Midjourney Bot. **Jobs  **include using
`/imagine` to create an initial image grid, upscaling images, and creating
variations of images.

The Midjourney Bot processes jobs on high-end GPUs. Each minute that it takes
to complete a job is a **GPU minute**. You have a limited amount of GPU
minutes when in **Fast Mode**. Because image generations may be processed on
multiple GPUs simultaneously, GPU minutes are not directly connected to the
time you wait for an image to generate.

* * *

__

Previous

Next

 __

Table of contents

![Midjourney
Logo](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_LogoType.png)

Midjourney is an independent research lab exploring new mediums of thought and
expanding the imaginative powers of the human species. We are a small self-
funded team focused on design, human infrastructure, and AI.

FOLLOW US: [[F]](//www.facebook.com/groups/officialmidjourney)
[[T]](//twitter.com/midjourney) [[R]](//www.reddit.com/r/midjourney/)

Support

For questions or support visit the [ Midjourney Discord support
channels](//discord.com/channels/662267976984297473/958069758211797092/).

Sites

  * [Midjourney Website](//midjourney.com/)
  * [Midjourney Discord](//discord.gg/midjourney)

__

[
![Midjourney](//cdn.document360.io/logo/3040c2b6-fead-4744-a3a9-d56d621c6c7e/778d06e9a335497ba965629e3b83a31f-MJ_Boat.png)
](/)

  * [__](/v1/en)

Contents x

No matching results found

  * 

* * *

__ __

Image Prompts

  *  __ Dark

 __ Light

 __Contents

# Image Prompts

  *  __ Dark

 __ Light

* * *

Article summary

 __

Did you find this summary helpful? __ __ __ __

__

Thank you for your feedback

#### You can use images as part of a prompt to influence a Job's composition,
style, and colors. Images prompts can be used alone or with text
prompts—experiment with combining images with different styles for the most
exciting results.

To add images to a prompt, type or paste the web address where the image is
stored online. The address must end in an extension like .png, .gif, or .jpg.
After adding image addresses, add any additional text and parameters to
complete the prompt.

![Image showing the Midjourney prompt
structure.](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ%20Prompt.png)

  

  * Prompts must have multiple image prompts or a single image prompt and a text prompt to work.
  * An image URL must be a direct link to an online image.
  * Your file should end in .png, .gif, .webp, .jpg, or .jpeg.
  * In most browsers, right-click or long-press an image and select Copy Image Address to get the URL.
  * The [`/blend` command](/blend) is a simplified image prompting process optimized for mobile users.
  * You can also use image URLs as [Style References](/v1/docs/style-reference) or [Character References](/v1/docs/character-reference).

  

Privacy Notes

  * Upload images in your direct messages with the Midjourney Bot to prevent other server users from seeing an image.
  * Image prompts and references are visible on the Midjourney website unless you're generating in [Stealth Mode](/v1/docs/stealth).

  

* * *

## How to Use an Image in Your Prompt

### 1\. Upload an image to Discord

[Follow these instructions to upload your image to
Discord.](//support.discord.com/hc/en-us/articles/211866427-How-do-I-upload-
images-and-GIFs)

  

### 2\. Copy your image's URL

*Discord Desktop App: Right-click on the image and select **Copy Link** (NOT "Copy Message Link").

  * Discord Web App: Click to expand the image, then right-click and choose "Copy image address."
  * Discord Mobile App: Tap and hold on the image, then select "Copy Media Link."

If none of these methods work, you can click to expand the image, and at the
bottom, select "Open in Browser" so you can copy and paste the image's URL.

To incorporate an image into your prompt, you need a direct image link that
ends with .png, .gif, .webp, .jpg, or .jpeg. If the image is on your computer
or phone, you can send it as a message to the Midjourney Bot first to generate
a link.

### How To Upload Your Image

## Add an Image URL to Your Prompt

To add an image to a prompt, begin typing `/imagine` as usual. After the
prompt box appears, drag the image file into the prompt box to add the image's
URL, or right-click and paste the link within the prompt box.

![Discord_FHZfwDLhLY.gif](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/Discord_FHZfwDLhLY.gif)

  

* * *

## Examples

### Starting Images

![Cropped image of a greecian statue generated with
Midjourney](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_ImagePrompt_Statue.png)

Greecian style statue

![Cropped image of vintage flower
illustraiton](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_ImagePrompt_Flowers.png)

Vintage Flower Illustration

![Cropped image of Ernst Haeckel's
Jellyfish](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_ImagePrompt_Jelly.jpg)

Ernst Haeckel's Jellyfish

![Cropped image of Ernst Haeckel's
Lichen](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_ImagePrompt_Lichen.png)

Ernst Haeckel's Lichen

![Cropped image of The Great Wave off
Kanagawa](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_ImagePrompt_Wave.png)

Hokusai's The Great Wave

  

### Midjourney Model Version 5

### Statue + Flowers

![Cropped image of the Bust of
Apollo](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_ImagePrompt_Statue.png)
\+ ![Cropped image of vintage flower
illustraiton](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_ImagePrompt_Flowers.png)

![Midjourney image prompt combining  a greecian style statue and a cropped
section of a vintage illustration of cyclamen
flowers](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_ImagePrompt_Statue_Flowers.jpg)

### Statue + Jellyfish

![Cropped image of the Bust of
Apollo](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_ImagePrompt_Statue.png)
\+ ![Cropped image of Ernst Haeckel's
Jellyfish](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_ImagePrompt_Jelly.jpg)
![Midjourney image prompt combining  a greecian style statue and a cropped
section of jellyfish by Ernst
Haeckel's](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_ImagePrompt_Statue_Jelly.jpg)

### Statue + Lichen

![Cropped image of the Bust of
Apollo](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_ImagePrompt_Statue.png)
\+ ![Cropped image of Ernst Haeckel's
Lichen](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_ImagePrompt_Lichen.png)
![Midjourney image prompt combining  a greecian style statue and a cropped
section of lichen by Ernst
Haeckel's](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_ImagePrompt_Statue_Lichen.jpg)

### Statue + Wave

![Cropped image of the Bust of
Apollo](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_ImagePrompt_Statue.png)
\+ ![Cropped image of The Great Wave off
Kanagawa](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_ImagePrompt_Wave.png)
![Midjourney image prompt combining  a greecian style statue and a cropped
section of the Great Wave off Kanagawa by
Hokusai](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_ImagePrompt_Statue_Wave.jpg)

### Statue + Lichen + Flowers

![Cropped image of the Bust of
Apollo](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_ImagePrompt_Statue.png)
\+ ![Cropped image of Ernst Haeckel's
Lichen](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_ImagePrompt_Lichen.png)
\+ ![Cropped image of vintage flower
illustraiton](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_ImagePrompt_Flowers.png)
![Midjourney image prompt combining  a greecian style statue, a cropped
section of lichen by Ernst Haeckel's, and a vintage floral
illustration](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_ImagePrompt_Statue_Flowers_Lichen.jpg)

  

Aspect Ratio Tip

Crop images to the same aspect ratio as your final image for the best results.

  

* * *

## Image Weight Parameter

Use the image weight parameter `--iw` to adjust the importance of the image
vs. text portion of a prompt. The default value is used when no `--iw` is
specified. Higher `--iw` values mean the image prompt will have more impact on
the finished job.

See the [Multi Prompts](/multi-prompts) page for more information about the
relative importance between parts of a prompt.

Different [Midjourney Version Models](/models) have different image weight
ranges.

| Version 6| Version 5| Version 4| niji 6| niji 5  
---|---|---|---|---|---  
Image Weight Default| 1| 1| NA| 1| 1  
Image Weight Range| 0–3| 0–2| NA| 0–3| 0–2  
  
  

prompt example: `/imagine prompt` `flowers.jpg birthday cake --iw .5`

![Cropped image of painter Jan Davidsz de Heem's Vase of Flowers used a
midjourney image
prompt](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/mj_iw-
start.jpg)

Image Prompt

![A midjourney image generated from an image prompt of an oil painting of
flowers and the prompt, a birthday cake with the image weight parameter set to
0.25](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/mj_iw-025.jpg)

\--iw .25

![A midjourney image generated from an image prompt of an oil painting of
flowers and the prompt, a birthday cake with the image weight parameter set to
0.5](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/mj_iw-050.jpg)

\--iw .5

![A midjourney image generated from an image prompt of an oil painting of
flowers and the prompt, a birthday cake with the image weight parameter set to
0.75](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/mj_iw-075.jpg)

\--iw .75

![A midjourney image generated from an image prompt of an oil painting of
flowers and the prompt, a birthday cake with the image weight parameter set to
1.0](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/mj_iw-100.jpg)

\--iw 1

![A midjourney image generated from an image prompt of an oil painting of
flowers and the prompt, a birthday cake with the image weight parameter set to
1.25](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/mj_iw-125.jpg)

\--iw 1.25

![A midjourney image generated from an image prompt of an oil painting of
flowers and the prompt, a birthday cake with the image weight parameter set to
1.5](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/mj_iw-150.jpg)

\--iw 1.5

![A midjourney image generated from an image prompt of an oil painting of
flowers and the prompt, a birthday cake with the image weight parameter set to
1.75](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/mj_iw-175.jpg)

\--iw 1.75

![A midjourney image generated from an image prompt of an oil painting of
flowers and the prompt, a birthday cake with the image weight parameter set to
2.0](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/mj_iw-200.jpg)

\--iw 2

![A midjourney image generated from an image prompt of an oil painting of
flowers and the prompt, a birthday cake with the image weight parameter set to
2.0](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/mj_iw-300.jpg)

\--iw 3

  

* * *

## Technical Details

Prompts that only use images and no text are not compatible with the
[\--stylize](/stylize), or [\--weird](/weird) parameters.

* * *

__

Previous

Next

 __

Table of contents

![Midjourney
Logo](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_LogoType.png)

Midjourney is an independent research lab exploring new mediums of thought and
expanding the imaginative powers of the human species. We are a small self-
funded team focused on design, human infrastructure, and AI.

FOLLOW US: [[F]](//www.facebook.com/groups/officialmidjourney)
[[T]](//twitter.com/midjourney) [[R]](//www.reddit.com/r/midjourney/)

Support

For questions or support visit the [ Midjourney Discord support
channels](//discord.com/channels/662267976984297473/958069758211797092/).

Sites

  * [Midjourney Website](//midjourney.com/)
  * [Midjourney Discord](//discord.gg/midjourney)

__

[
![Midjourney](//cdn.document360.io/logo/3040c2b6-fead-4744-a3a9-d56d621c6c7e/778d06e9a335497ba965629e3b83a31f-MJ_Boat.png)
](/)

  * [__](/v1/en)

Contents x

No matching results found

  * 

* * *

__ __

Style Tuner

  *  __ Dark

 __ Light

 __Contents

# Style Tuner

  *  __ Dark

 __ Light

* * *

Article summary

 __

Did you find this summary helpful? __ __ __ __

__

Thank you for your feedback

#### Personalize the appearance of your Midjourney images using the Style
Tuner. Use the /tune command to generate a range of sample images showing
different visual styles based on your prompt. Choose your favorite images, and
you'll receive a unique code you can use to customize the look of future Jobs.

Share your Style Tuner and Codes with others to share, explore, and experiment
with different aesthetics.

**`/tune` and codes are only compatible with [Midjourney Model Version
5.2](/models)**  
**`/tune` is not compatible with the current default [Midjourney Model Version
6](/models)**  
`/tune` is only available while in Fast Mode.  
`--style` parameters created with the Style Tuner are compatible with
`--stylize` values between 20–1000.

  

* * *

## How to Use the Style Tuner

### 1\. Generate Your Custom Style Tuner

Create a Style Tuner page using the `/tune` command.

![TuneGif](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/TuneGif.gif)

  

### 2\. Select Your Preferred Options

  * **Style Directions:** Choose the number of image pairs you want to see in your Style Tuner (16, 32, 64, or 128 pairs).
  * **Default Mode:** Select the [style](/style) mode for your sample images (Default or Raw). If you typically do not use the --style raw parameter with your prompts, choose "default."

![MJ_CreateStyleTuner](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_CreateStyleTuner.png)

Use an Exisiting Style Tuner

If another user has previously generated a Style Tuner with your prompt, you
will receive a link to that Tuner. Click the link to access the existing Style
Tuner. Using a previously generated Style Tuner does not use your
subscription's GPU minutes.

  

### 3\. Submit your Job

  * Click the `Submit` button.
  * Confirm your submission.

![Image showing this dialog box created after using the Midjourney tune
command. An arrow is pointing to the Submit
button](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_StyleTuner_Submit.png)

![Image showing this dialog box created after using the Midjourney tune
command. An arrow is pointing to the Are You Sure
button](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_StyleTuner_Confirm.png)

Your Style Tuner generates a pair of images for each Style Direction. A Style
Tuner with 16 directions will generate 32 images. A Style Tuner with 128
directions will generate 256 images. Generating these images uses your
subscription's Fast GPU time.

  

### 4\. Open Your Custom Style Tuner

  * When your Style Tuner is ready, the Midjourney Bot will send you a [direct message](/direct-messages) with a link to your Tuner.
  * Click the link to open your Style Tuner in your web browser.

![Image showing this dialog box created after the Midjourney Bot has returned
a link to your Style Tuner
page](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_StyleTuner_Ready.png)

Try this Style Tuner:
[https://tuner.midjourney.com/ejYLCOY](//tuner.midjourney.com/ejYLCOY)

  

### 5\. Select images

Your Style Tuner will show rows of image pairs, each representing a distinct
visual direction for your prompt. Click on the image you prefer in each pair.
If you don't feel strongly about either image, leave the empty middle box
selected.

![Image showing the Midjourney Style Tuner webpage where users choose from
pairs of
images](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_StyleTuner_ImagePairs.png)

  

### 6\. Copy Your Code

The Style Tuner generates a code you can add to your prompts with the `--style
<code>` Parameter. [Learn more about parameters.](/parameter-list)

**To copy your prompt and Parameter**

  * Find your customized code at the bottom of the page.
  * Click the `Copy` button to copy your original prompt and newly generated `--style <code>` parameter.

You can share your Style Tuner page with friends and generate new codes
without using any additional GPU minutes!

![Image showing the Midjourney Style Tuner webpage show the location of the
copy code
button](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_StyleTuner_CopyCode.png)

  

### 7\. Generate an Image

  * Return to Discord
  * Use the `/imagine` command and paste your copied prompt and `--style <code>` parameter into the `prompt` field.
  * Generate your image

![Image showing the Midjourney Prompt Box with the text vibrant California
poppies --code
eS9PCegXqCuxjAm](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_StyleTuner_Prompt.png)

![Image showing the Midjourney interface with a grid of images made with the
prompt vibrant California poppies --code
E9qe0kNB](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_StyleTuner_Results.png)

  

### 8\. Use Additional Midjourney Tools

Take your image further by using other Midjourney tools like
[Upscale](/upscalers), [Pan](/pan), [Zoom-Out](/zoom-out), [Remix](/remix), or
[Vary-Region](/vary-region).

  

### 9\. Experiment and Explore

Use your style code with a new prompt:

The Style Tuner you create uses your initial prompt to create sample images
and help you visualize the impact of your choices. However, the generated
codes can be used with any prompt. Remember that styles and prompts always
work together to generate an image, so a style code may not transfer as
intended to other prompts.

  * **Experiment:** Style codes and prompts interact in complex ways. A code may have a strong effect on one prompt and a subtle effect on a similar prompt. The images you choose in your Style Tuner can combine in unexpected and creative ways. Use style codes as a tool to explore new looks and visuals.
  * **Generate more codes:** You can return to your Style Tuner page at any time to change your selections and create new codes.
  * **Share style codes:** You can share or use style codes created by friends.
  * **Find a Style Tuner page:** Find the Style Tuner page for any style code by adding it to this URL: https://tuner.midjourney.com/code/StyleCodeHere.

  

### 10\. Save and Reuse Your Codes

  * Use the `/settings` command and turn on `📌Sticky Style`. Sticky Style will save the last `--style` parameter used in your personal suffix, so you don't have to repeat the code on future prompts. Change codes by using a new `--style` or unselecting `📌Sticky Style`.
  * Use [custom options](//docs.midjourney.com/docs/settings-and-presets#custom-preferences) to store your favorite codes.
  * Or, [create your own Discord server](//support.discord.com/hc/en-us/articles/204849977-How-do-I-create-a-server-) to organize your images, prompts, image references, and Style Tuner codes.

  

* * *

## Style Tune Examples

`prompt` `vibrant california poppies`  
All images were made by style created using this [Style
Tuner](//tuner.midjourney.com/ejYLCOY)

![Midjourney image grid made with the prompt vibrant California
poppies](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_StyleTuner_Original.jpg)

![Midjourney image grid made with the prompt vibrant California poppies
--style
smBcOlvkn](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_StyleTuner_smBcOlvkn.jpg)

![Midjourney image grid made with the prompt vibrant California poppies
--cstyle code
kaxBt2Ez](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_StyleTuner_kaxBt2Ez.jpg)

![Midjourney image grid made with the prompt vibrant California poppies
--style
cFXCdj6b](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_StyleTuner_cFXCdj6b.jpg)

![Midjourney image grid made with the prompt vibrant California poppies
--style
74BORIhDi7lN](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_StyleTuner_74BORIhDi7lN.jpg)

![Midjourney image grid made with the prompt vibrant California poppies
--style
9E9f1kv9V3t](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_StyleTuner_9E9f1kv9V3t.jpg)

![Midjourney image grid made with the prompt vibrant California poppies
--style
6qOiawNR](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_StyleTuner_6qOiawNR.jpg)

![Midjourney image grid made with the prompt vibrant California poppies
--style
4hWWZ8koe2PN](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_StyleTuner_4hWWZ8koe2PN.jpg)

![Midjourney image grid made with the prompt vibrant California poppies
--style
4hWWZ8koe2PN](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_StyleTuner_S0.jpg)

![Midjourney image grid made with the prompt vibrant California poppies
--style
BjRnPd4xaz](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_StyleTuner_BjRnPd4xaz.jpg)

![Midjourney image grid made with the prompt vibrant California poppies
--style
2cV4IG7MDkNd](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_StyleTuner_2cV4IG7MDkNd.jpg)

![Midjourney image grid made with the prompt vibrant California poppies
--style
2f582Pa6gvbt](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_StyleTuner_2f582Pa6gvbt.jpg)

  

* * *

## Random Codes

Use the `--style random` parameter to apply a random 32 base styles Style
Tuner code to your prompt. You can also use `--style random-16`, `--style
random-64` or `--style random-128` to use random results from other lengths of
tuners.

`--random` simulates Style Tuner code with random selections chosen for 75% of
the image pairs. You can adjust this percentage by adding a number to the end
of the `--random` parameter. For example, `--style random-32-15` simulates a
32-pair tuner with 15% of the image pairs selected, `--style random-128-80`
simulates a 128-pair tuner with 80% of the image pairs selected.

  

* * *

## Combine Codes

Combine multiple codes in one parameter with a hyphen, `--style code1-code2`.  
Combine multiple codes and style raw: `--style raw-code1-code2`

  

* * *

## Style Tuner and --stylize

The [`--stylize` parameter](/stylize) adjusts the influence of the --style
parameter on your generated images. If you're not seeing the desired effect
from your code, consider combining it with higher stylization values, like
`--stylize 250`, or `--stylize 500`.

### Comparison

`prompt` `vibrant California poppies --style fdeQ4zOX5jd --stylize 250`

![Midjourney image grid made with the prompt vibrant California poppies
--style 4hWWZ8koe2PN --s
20](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_StyleTuner_S0.jpg)

\--stylize 20

![Midjourney image grid made with the prompt vibrant California poppies
--style 4hWWZ8koe2PN --s
100](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_StyleTuner_S100.jpg)

\--stylize 100 (default)

![Midjourney image grid made with the prompt vibrant California poppies
--style 4hWWZ8koe2PN --s
250](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_StyleTuner_S250.jpg)

\--stylize 250

![Midjourney image grid made with the prompt vibrant California poppies
--style 4hWWZ8koe2PN --s
750](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_StyleTuner_750.jpg)

\--stylize 750

  

* * *

## Style Raw

Combine your custom style code with Midjourney Style Raw by using `--style
raw-<code>`.  
Example: To use Style Raw and `--style fjo5S8BgMoV` use `--style raw-
fjo5S8BgMoV`.

  

* * *

## Style Tuner and Niji Model Version

Style Tuner codes created with the Midjourney Bot are not compatible with the
[Niji Model version](/models) accessed through the Midjourney Bot. To create a
Style Tuner or Code for Niji Model version, join the [Niji Discord
community](//discord.com/invite/nijijourney) and interact with the Niji Bot in
the same way you interact with the Midjourney Bot. Your Midjourney
subscription gives you access to the Niji community and Bot.

  

* * *

## Technical Details

`/tune` is compatible with prompts that include the following:  
\--aspect  
\--chaos  
\--tile  
[multi prompts](/multi-prompts)

`/tune` and style codes are not compatible with [image prompts](/image-
prompts) that do not include a text prompt.

  
  
If your `/tune` command does not return a clickable link, check that **Embeds
and Link Previews** is enabled in your Discord **App Settings**  
![an image showing the discord text and image setting and enable link preview
toggle set to to
on](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_AppSettings_Embed.png)

  

* * *

There are two modes for image generation, **Fast Mode** and**  Relax Mode**.
Fast Mode tries to give you a GPU instantly. It's the highest-priority
processing tier and uses your subscription's monthly GPU time. **Relax Mode**
queues your generation behind others based on how much you've used the system.
**Relax Mode** wait times are variable and usually range from 1-10 minutes.

By default, your images will be generated using **Fast** mode. You can switch
to **Relax  **if you have a Standard or Pro subscription.

There are two modes for image generation, **Fast Mode** and**  Relax Mode**.
Fast Mode tries to give you a GPU instantly. It's the highest-priority
processing tier and uses your subscription's monthly GPU time. **Relax Mode**
queues your generation behind others based on how much you've used the system.
**Relax Mode** wait times are variable and usually range from 1-10 minutes.

By default, your images will be generated using **Fast** mode. You can switch
to **Relax  **if you have a Standard or Pro subscription.

Parameters are options added to a prompt that change how an image generates.
Parameters can change an image's Aspect Ratios, switch between Midjourney
Model Versions, change which Upscaler is used, and lots more.

* * *

__

Previous

Next

 __

Table of contents

![Midjourney
Logo](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_LogoType.png)

Midjourney is an independent research lab exploring new mediums of thought and
expanding the imaginative powers of the human species. We are a small self-
funded team focused on design, human infrastructure, and AI.

FOLLOW US: [[F]](//www.facebook.com/groups/officialmidjourney)
[[T]](//twitter.com/midjourney) [[R]](//www.reddit.com/r/midjourney/)

Support

For questions or support visit the [ Midjourney Discord support
channels](//discord.com/channels/662267976984297473/958069758211797092/).

Sites

  * [Midjourney Website](//midjourney.com/)
  * [Midjourney Discord](//discord.gg/midjourney)

__

[
![Midjourney](//cdn.document360.io/logo/3040c2b6-fead-4744-a3a9-d56d621c6c7e/778d06e9a335497ba965629e3b83a31f-MJ_Boat.png)
](/)

  * [__](/v1/en)

Contents x

No matching results found

  * 

* * *

__ __

Chaos

  *  __ Dark

 __ Light

 __Contents

# Chaos

  *  __ Dark

 __ Light

* * *

Article summary

 __

Did you find this summary helpful? __ __ __ __

__

Thank you for your feedback

#### The `--chaos` or `--c` parameter influences how varied the initial image
grids are. High `--chaos` values will produce more unusual and unexpected
results and compositions. Lower `--chaos` values have more reliable,
repeatable results.

`--chaos` accepts values 0–100.  
The default `--chaos` value is 0.

* * *

## The Influence of Chaos on Jobs

### No `--chaos` value

Using a very low `--chaos` value, or not specifying a value, will produce
initial image grids that are similar.

prompt example: `/imagine prompt:` `a silver seashell inlaid with pink and
green accents --c 0`

![A midjourney generated image generated from the prompt, a silver seashell
inlaid with pink and green accents --c
0](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_Chaos_0a.jpg)

![A midjourney generated image generated from the prompt, a silver seashell
inlaid with pink and green accents --c
0](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_Chaos_0b.jpg)

![A midjourney generated image generated from the prompt, a silver seashell
inlaid with pink and green accents --c
0](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_Chaos_0c.jpg)

  

### Low `--chaos` values

Using a low `--chaos` value will produce initial image grids that are slightly
varied.

prompt example: `/imagine prompt:` `a silver seashell inlaid with pink and
green accents --c 10`

![A midjourney generated image generated from the prompt, a silver seashell
inlaid with pink and green accents --c
10](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_Chaos_10a.jpg)

![A midjourney generated image generated from the prompt, a silver seashell
inlaid with pink and green accents --c
10](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_Chaos_10b.jpg)

![A midjourney generated image generated from the prompt, a silver seashell
inlaid with pink and green accents --c
10](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_Chaos_10c.jpg)

  

### Moderate `--chaos` values

Using a moderate `--chaos` value will produce initial image grids that are
varied.

prompt example: `/imagine prompt:` `a silver seashell inlaid with pink and
green accents --c 25`

![A midjourney generated image generated from the prompt, a silver seashell
inlaid with pink and green accents --c
25](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_Chaos_25a.jpg)

![A midjourney generated image generated from the prompt, a silver seashell
inlaid with pink and green accents --c
25](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_Chaos_25b.jpg)

![A midjourney generated image generated from the prompt, a silver seashell
inlaid with pink and green accents --c
25](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_Chaos_25c.jpg)

  

### High `--chaos` Values

Using a higher `--chaos` value will produce initial image grids that are more
varied and unexpected.

prompt example: `/imagine prompt:` `a silver seashell inlaid with pink and
green accents --c 50`

![A midjourney generated image generated from the prompt, a silver seashell
inlaid with pink and green accents --c
50](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_Chaos_50a.jpg)

![A midjourney generated image generated from the prompt, a silver seashell
inlaid with pink and green accents --c
50](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_Chaos_50b.jpg)

![A midjourney generated image generated from the prompt, a silver seashell
inlaid with pink and green accents --c
50](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_Chaos_50c.jpg)

  

### Very High `--chaos` Values

Using extremely high `--chaos` values will produce initial image grids that
are varied and have unexpected compositions or elements.

prompt example: `/imagine prompt:` `a silver seashell inlaid with pink and
green accents --c 80`

![A midjourney generated image generated from the prompt, a silver seashell
inlaid with pink and green accents --c
80](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_Chaos_80a.jpg)

![A midjourney generated image generated from the prompt, a silver seashell
inlaid with pink and green accents --c
80](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_Chaos_80b.jpg)

![A midjourney generated image generated from the prompt, a silver seashell
inlaid with pink and green accents --c
80](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_Chaos_80c.jpg)

* * *

## How to Change the Chaos Value

### Use the `--chaos` or `--c` Parameter

Add `--chaos <value>` or `--c <value>` to the end of your prompt on Discord or
in the imagine bar on the website:

![Animated Gif showing how the Midjourney chaos parameter is
typed](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_Parameter_Chaos.gif)

  

### Website Settings

On the website imagine bar Settings, Chaos is called Variety. You can set a
default Variety value using the Settings button in the imagine bar:

![](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/mj-
website-settings-chaos.png)

  

Adjust the slider left for lower values and right for higher values.

The value you set here will apply to all your prompts unless you specify a
different value using the `--chaos` or `--c` parameter in an individual
prompt.

* * *

__

Previous

Next

 __

Table of contents

![Midjourney
Logo](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_LogoType.png)

Midjourney is an independent research lab exploring new mediums of thought and
expanding the imaginative powers of the human species. We are a small self-
funded team focused on design, human infrastructure, and AI.

FOLLOW US: [[F]](//www.facebook.com/groups/officialmidjourney)
[[T]](//twitter.com/midjourney) [[R]](//www.reddit.com/r/midjourney/)

Support

For questions or support visit the [ Midjourney Discord support
channels](//discord.com/channels/662267976984297473/958069758211797092/).

Sites

  * [Midjourney Website](//midjourney.com/)
  * [Midjourney Discord](//discord.gg/midjourney)

__

[
![Midjourney](//cdn.document360.io/logo/3040c2b6-fead-4744-a3a9-d56d621c6c7e/778d06e9a335497ba965629e3b83a31f-MJ_Boat.png)
](/)

  * [__](/v1/en)

Contents x

No matching results found

  * 

* * *

__ __

Model Version 5

  *  __ Dark

 __ Light

 __Contents

# Model Version 5

  *  __ Dark

 __ Light

* * *

Article summary

 __

Did you find this summary helpful? __ __ __ __

__

Thank you for your feedback

#### Midjourney regularly introduces new model versions to improve coherency,
efficiency, quality, and style. You can switch model versions by using the
[/settings command](/settings-and-presets) and selecting your preferred model
version. Different models excel at producing different types of images.

#### [Read about the latest Midjourney Models here.](/models)

* * *

## Default Parameter Values

Model Version 5, 5.1, and 5.2

| Aspect Ratio| Chaos| Quality| Seed| Stop| Stylize  
---|---|---|---|---|---|---  
Default Value  
| 1:1| 0| 1| Random| 100| 100  
Range  
| any| 0–100| .25 .5, or 1| whole numbers 0–4294967295| 10–100| 0–1000  
  
  * Aspect ratios greater than 2:1 are experimental and may produce unpredictable results.

  

* * *

## Model Version 5.2 (Legacy)

The Midjourney V5.2 model was released in June 2023. To use this model, add
the `--v 5.2` parameter to the end of a prompt, or use the `/settings` command
and select `5️⃣ MJ Version 5.2`

Default Model 06/22/23–02/14/2024

This model produces more detailed, sharper results with better colors,
contrast, and compositions. It also has a slightly better understanding of
prompts than earlier models and is more responsive to the full range of the
[`--stylize` parameter](/stylize).

  

![Midjourney Version 5.2 example image of the prompt Vibrant California
Poppies](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_V52_VibrantPoppies.jpg)

Prompt: vibrant California poppies --v 5.2

![Midjourney Version 5.2 example image of the prompt high contrast surreal
collage](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_V52_HighContrastCollage.jpg)

Prompt: high contrast surreal collage --v 5.2

  

### Model Version 5.2 + Style Raw Parameter

Midjourney Model Versions 5.1 and 5.2 can be fine-tuned with the `--style raw`
parameter to reduce the Midjourney default aesthetic.

[Read more about the Midjourney `--style` parameter.](/style)

  

##### `default --v 5.2`

![Midjourney Version v5.2 example image of the prompt vibrant california
poppies --v
5.2](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_V52_Poppies.jpg)
`vibrant California poppies`

##### `--v 5.2 --style raw`

![Midjourney Version v5.2 example image of the prompt vibrant california
poppies --v
5.2](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_V52_Poppies_RAW.jpg)
`vibrant California poppies --style raw`

##### `default --v 5.2`

![Midjourney Version v5.2 example image high contrast surreal collage --v
5.2](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_V52_SurrealCollage.jpg)
`high contrast surreal collage`

##### `--v 5.2 --style raw`

![Midjourney Version v5.2 example image high contrast surreal collage --v
5.2](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_V52_SurrealCollage_RAW.jpg)
`high contrast surreal collage --style raw`

  

* * *

## Model Version 5.1 (Legacy)

The Midjourney V5.1 was released on May 4th, 2023. To use this model, add the
`--v 5.1` parameter to the end of a prompt, or use the `/settings` command and
select `5️⃣ MJ Version 5.1`

Default Model 05/03/23–06/22/23

This model has a stronger default aesthetic than earlier versions, making it
easier to use with simple text prompts. It also has high Coherency, excels at
accurately interpreting natural language prompts, produces fewer unwanted
artifacts and borders, has increased image sharpness, and supports advanced
features like repeating patterns with [`--tile`](/tile).

  

![Midjourney Version 5.1 example image of the prompt Vibrant California
Poppies](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_V51_VibrantPoppies.jpg)

Prompt: vibrant California poppies --v 5.1

![Example image created with the Midjourney v5 algorithm using the Prompt:
high contrast surreal
collage](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_V51_HighContrastCollage.jpg)

Prompt: high contrast surreal collage --v 5.1

  

* * *

## Model Version 5.0 (Legacy)

The Midjourney V5.0 model produces more photographic generations than the V5.1
model. This model produces images that closely match the prompt but may
require longer prompts to achieve your desired aesthetic.

Default Model 03/30/23–05/03/23

To use this model, add the `--v 5` parameter to the end of a prompt, or use
the `/settings` command and select `5️⃣ MJ Version 5`  
  

![Midjourney Version 5 example image of the prompt Vibrant California
Poppies](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_V5_VibrantCaliforniaPoppies.png)

Prompt: vibrant California poppies --v 5

![Example image created with the Midjourney v5 algorithm using the Prompt:
high contrast surreal
collage](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_V5_HighContrastCollage.jpg)

Prompt: high contrast surreal collage --v 5

  

  

* * *

## Niji Model 5 (Legacy)

The Niji model is a collaboration between Midjourney and
[Spellbrush](//spellbrush.com/) tuned to produce anime and illustrative styles
with vastly more knowledge of anime, anime styles, and anime aesthetics. It's
excellent at dynamic and action shots and character-focused compositions.

To use this model, add the `--niji 5` parameter to the end of a prompt, or use
the `/settings` command and select `🍏 Niji version 5`

This model is sensitive to the [`--stylize` parameter](/docs/stylize).
Experiment with different stylization ranges to fine-tune your images.

### Niji 5 Styles

[Niji Model Version 5](/models) can also be fine-tuned with `--style`
parameters to achieve unique looks. Try `--style cute`, `--style scenic`,
`--style original` (uses the original Niji Model Version 5, which was the
default before May 26th, 2023), or `--style expressive`.

**Niji Style Parameters**  
`--style cute` creates charming and adorable characters, props, and settings.  
`--style expressive` has a more sophisticated illustrated feeling.  
`--style original` uses the original Niji Model Version 5, which was the
default before May 26th, 2023.  
`--style scenic` makes beautiful backgrounds and cinematic character moments
in the context of their fantastical surroundings.

##### `default --niji 5`

![Midjourney Version v5 example image of the prompt birds perching on a branch
--niji
5](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_Niji5.jpg)

birds perching on a twig --niji 5

##### `--style original`

![Midjourney Version v5 example image of the prompt birds perching on a branch
--style original--niji
5](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_Niji5_Original.jpg)

birds perching on a twig --niji 5 --style original

##### `--style cute`

![Midjourney Version v5 example image of the prompt birds perching on a branch
--niji 5 --style
cute](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_Niji5_cute.jpg)

birds perching on a twig --niji 5 --style cute

##### `--style expressive`

![Midjourney Version v5 example image of the prompt birds perching on a branch
--niji 5 --style
expressive](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_Niji5_expressive.jpg)

birds perching on a twig --niji 5 --style expressive

##### `--style scenic`

![Midjourney Version v5 example image of the prompt birds perching on a branch
--niji 5 --style
scenic](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_Niji5_scenic.jpg)

birds perching on a twig --niji 5 --style scenic

  

* * *

## V5 Upscaler Tools

Midjourney Model Version 5.2 produces grids of 1024 x 1024 pixel images. Use
the `U1` `U2` `U3` `U4` buttons under each image grid to separate your
selected image from its grid. You can then use the `Upscale (2x)` or `Upscale
(4x)` tools to increase the size of your image.

`Upscale` tools use your subscription's GPU minutes. Using `Upscale 2X` on an
image takes roughly twice as long as generating an initial image grid. Using
`Upscale 4X` on an image takes roughly six times as long as generating an
initial image grid.

V5 `Upscale` tools are not compatible with the [pan](/pan) tool or the [tile
parameter](/tile).

  

### Upscaler Comparison

`Upscale (2x)`

Original 1024 by 1024 pixel image

![Midjourney Image created with prompt Chiaroscuro rooster
portrait](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_V52_Upscale_Chicken_Original.jpg)

Detail from the original image

![Detail of a Midjourney Image created with prompt Chiaroscuro rooster
portrait](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_V52_Upscale_Chicken_Up1X.jpg)

After `Upscale (2x)` to 2048 x 2048 px

![Detail of a Midjourney Image created with prompt Chiaroscuro rooster
portrait](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_V52_Upscale_Chicken_Up2X.jpg)

  

* * *

### Upscaler Comparison

Prompt: `1960s pop-art acrylic of redwoods`  
Original 1024 by 1024 pixel image.

Original 1024 by 1024 pixel image

![Midjourney Image created with prompt 1960s pop-art acrylic of
redwoods](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_V52_Upscale_Muir_Original.jpg)

Detail from the original image

![Cropped Midjourney Image created with prompt 1960s pop-art acrylic of
redwoods](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_V52_Upscale_Muir_Up1X.jpg)

After `Upscale (4x)` to 4096 x 4096 px

![Cropped Midjourney Image created with prompt 1960s pop-art acrylic of
redwoods after
upscaling](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_V52_Upscale_Muir_Up4X.jpg)

  

* * *

## Influence of [\--stylize](/stylize) on Model Version 5

### Midjourney Model Version 5 [Stylize](/stylize) Comparison

prompt example: `/imagine prompt` `child's drawing of a cat --s 100`

##### `--stylize 50`

![Midjourney style parameter example. Image of the prompt childs drawing of a
cat
stylize=0](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/stylize_v52_Childcat_50.jpg)
Equal to `🖌️ Style Low`

##### `--stylize 100` (default)

![Midjourney style parameter example. Image of the prompt childs drawing of a
cat
stylize=100](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/stylize_v52_Childcat_100.jpg)
Equal to `🖌️ Style Med`

##### `--stylize 250`

![Midjourney style parameter example. Image of the prompt childs drawing of a
cat
stylize=250](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/stylize_v52_Childcat_250.jpg)
Equal to `🖌️ Style High`

##### `--stylize 750`

![Midjourney style parameter example. Image of the prompt childs drawing of a
cat
stylize=750](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/stylize_v52_Childcat_750.jpg)
Equal to `🖌️ Style Very High`

  

### Niji 5 [Stylize](/stylize) Comparison

prompt example: `/imagine prompt` `colorful risograph of a fig --niji 5 --s
100`

`--stylize 50`

![Midjourney style parameter example. Image of the prompt colorful risograph
of a fig
stylize=50](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_Stylize_Niji5_50.jpg)
`🖌️ Style Low`

`--stylize 100` (default)

![Midjourney style parameter example. Image of the prompt colorful risograph
of a fig
stylize=100](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_Stylize_Niji5_100.jpg)
`🖌️ Style Med`

`--stylize 250`

![Midjourney style parameter example. Image of the prompt colorful risograph
of a fig
stylize=250](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_Stylize_Niji5_250.jpg)
`🖌️ Style High`

`--stylize 750`

![Midjourney style parameter example. Image of the prompt colorful risograph
of a fig
stylize=750](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_Stylize_Niji5_750.jpg)
`🖌️ Style Very High`

  

**Coherency** is the strength of the connection between the text prompt and
the resulting image. A high degree of coherency means that the image will be
an accurate representation of the prompt text.

The Midjourney Bot processes jobs on high-end GPUs. Each minute that it takes
to complete a job is a **GPU minute**. You have a limited amount of GPU
minutes when in **Fast Mode**. Because image generations may be processed on
multiple GPUs simultaneously, GPU minutes are not directly connected to the
time you wait for an image to generate.

* * *

__

Previous

Next

 __

Table of contents

![Midjourney
Logo](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_LogoType.png)

Midjourney is an independent research lab exploring new mediums of thought and
expanding the imaginative powers of the human species. We are a small self-
funded team focused on design, human infrastructure, and AI.

FOLLOW US: [[F]](//www.facebook.com/groups/officialmidjourney)
[[T]](//twitter.com/midjourney) [[R]](//www.reddit.com/r/midjourney/)

Support

For questions or support visit the [ Midjourney Discord support
channels](//discord.com/channels/662267976984297473/958069758211797092/).

Sites

  * [Midjourney Website](//midjourney.com/)
  * [Midjourney Discord](//discord.gg/midjourney)

__

[
![Midjourney](//cdn.document360.io/logo/3040c2b6-fead-4744-a3a9-d56d621c6c7e/778d06e9a335497ba965629e3b83a31f-MJ_Boat.png)
](/)

  * [__](/v1/en)

Contents x

No matching results found

  * 

* * *

__ __

Prompts

  *  __ Dark

 __ Light

 __Contents

# Prompts

  *  __ Dark

 __ Light

* * *

Article summary

 __

Did you find this summary helpful? __ __ __ __

__

Thank you for your feedback

#### A prompt is a short text phrase that the Midjourney Bot interprets to
produce an image. The Midjourney Bot breaks down the words and phrases in a
prompt into smaller pieces, called tokens, that are compared to its training
data and then used to generate an image. A well-crafted prompt can help make
unique and exciting images.

## Basic Prompts

A basic prompt can be as simple as a single word, phrase or emoji 😊.

![Image showing the Midjourney prompt
structure.](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_Prompt_basic.png)

  

Prompting Tip!

The Midjourney Bot works best with simple, short phrases that describe what
you want to see. Avoid long lists of requests and instructions. Instead of:
**Show me a picture of lots of blooming California poppies, make them bright,
vibrant orange, and draw them in an illustrated style with colored pencils**
Try: **Bright orange California poppies drawn with colored pencils**

  

* * *

## Advanced Prompts

More advanced prompts can include one or more [image URLs](/image-prompts),
[multiple text phrases](/multi-prompts), and one or more
[parameters](/parameter-list)

![Image showing the Midjourney prompt
structure.](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ%20Prompt.png)

`Image Prompts`

Image URLs can be added to a prompt to influence the style and content of the
finished result. Image URLs always go at the front of a prompt.

[Read more about Image Prompts](/image-prompts)

`Text Prompt`

The text description of what image you want to generate. See below for
prompting information and tips. Well-written prompts help generate amazing
images.

`Parameters`

Parameters change how an image generates. Parameters can change aspect ratios,
models, upscalers, and lots more. Parameters go at the end of the prompt.

[Read more about Parameters](/parameter-list)

  

* * *

## Prompting Notes

### Word Choice

Word choice matters. More specific synonyms work better in many circumstances.
Instead of big, try huge, gigantic, enormous, or immense.

### Plural words and Collective Nouns

Plural words leave a lot to chance. Try specific numbers. "Three cats" is more
specific than "cats." Collective nouns also work, “flock of birds” instead of
"birds.”

### Focus on What You Want

It is better to describe what you want instead of what you don’t want. If you
ask for a party with “no cake,” your image will probably include a cake. To
ensure an object is not in the final image, try advanced prompting using the
[`--no` parameter](/multi-prompts).

### Prompt Length and Details

Prompts can be simple. A single word or emoji will work. However, short
prompts rely on Midjourney’s default style, allowing it to fill in any
unspecified details creatively. Include any element that is important to you
in your prompt. Fewer details means more variety but less control.

**Try to be clear about any context or details that are important to you.
Think about:**

  * **Subject:** _person, animal, character, location, object_
  * **Medium:** _photo, painting, illustration, sculpture, doodle, tapestry_
  * **Environment:** _indoors, outdoors, on the moon, underwater, in the city_
  * **Lighting:** _soft, ambient, overcast, neon, studio lights_
  * **Color:** _vibrant, muted, bright, monochromatic, colorful, black and white, pastel_
  * **Mood:** _sedate, calm, raucous, energetic_
  * **Composition:** _portrait, headshot, closeup, birds-eye view_

* * *

 __

Previous

Next

 __

Table of contents

![Midjourney
Logo](//cdn.document360.io/3040c2b6-fead-4744-a3a9-d56d621c6c7e/Images/Documentation/MJ_LogoType.png)

Midjourney is an independent research lab exploring new mediums of thought and
expanding the imaginative powers of the human species. We are a small self-
funded team focused on design, human infrastructure, and AI.

FOLLOW US: [[F]](//www.facebook.com/groups/officialmidjourney)
[[T]](//twitter.com/midjourney) [[R]](//www.reddit.com/r/midjourney/)

Support

For questions or support visit the [ Midjourney Discord support
channels](//discord.com/channels/662267976984297473/958069758211797092/).

Sites

  * [Midjourney Website](//midjourney.com/)
  * [Midjourney Discord](//discord.gg/midjourney)

__
