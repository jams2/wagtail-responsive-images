# wagtail-responsive-images

For an introduction to responsive images and the `<picture>` tag, see [MDN Web Docs](https://developer.mozilla.org/en-US/docs/Learn/HTML/Multimedia_and_embedding/Responsive_images). This library aims to provide a convenient way to include responsive images in [Wagtail](https://wagtail.io/) pages.

## Usage

### The `pset` template tag

The `pset` template tag expects the syntax

`{% pset IMAGE SPECS (attr=value)* [as VARNAME] %}`

where `IMAGE` is a Wagtail `Image` instance, `SPECS` are the image rendition specifications (more on this below). For example:

`{% pset image @sm(width-200),@md(width-500) alt="Foo bar baz" %}`

results in the following html being rendered:

```html

<picture>
    <source
        type="image/jpeg"
        srcset="/media/images/my-image.width-200.jpg"
        media="(max-width: 767px)"
    >
    <source
        type="image/jpeg"
        srcset="/media/images/my-image.fill-500x500.jpg"
        media="(max-width: 1023px)"
    >
    <img
        src="/media/images/my-image.fill-500x500.jpg"
        class=""
        loading="eager"
        alt="Foo bar baz"
    >
</picture>

```

Specifying `webp=True` will result in a webp rendition for each source element being included:

```html
<picture>
    <source
        type="image/webp"
        srcset="/media/images/my-image.width-200.format-webp.webp"
        media="(max-width: 767px)"
    >
    <source
        type="image/jpeg"
        srcset="/media/images/my-image.width-200.jpg"
        media="(max-width: 767px)"
    >
    ...
</picture>
```
