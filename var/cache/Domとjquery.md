[TOC]


------------
[javascript](/blog-backend/blog-view/?id=46 "javascript")

## window, navigator, location, history, document
- window
  - web storage API
    Window.localStorage
    Window.sessionStorage
	localStorageは保存されたデータの期限がないに対して、sessionStorageはセッション終了するとき消えます
	
	**メソット**
	length, key, getItem, setItem, deleteItem
	

tag: iframe, video, audio

#### navigator
| method | valueType | value |
| ----- | ----- |
| navigator.userAgent | string | Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36 |
| navigator.cookieEnabled | bool | true |
| navigator.onLine | bool | true |
| navigator.connection | object | downlink: 0.6,saveData: false... |
| navigator.language | string | en |

- location

| method | valueType | value |
| ----- | ----- |
| location.href | string |
| location.reload() | void |
| location.host | string | `location:1122` |
| location.origin | string | `http://location:1122` |
| location.pathname | string | `/a/b/c` |
| location.search | string | `?aa=2&bb=3` |
| location.protocol | string | `http:` |

- history
run to back, run to forward, run to any history page
history.back()
history.forward()
history.go(delta)

- document
**fullscreen:**

element fullscreen change

element.requestFullscreen()
documentElement.requestFullscreen()
document.exitFullscreen()

Document.fullscreenEnabled

event: onfullscreenchange

## css操作
#### css style
generation:
タグの前と後で内容を追加する
:before, :after--content
link:
:hover, :visited, :link, :active

- font
font-variant
font-variant-caps, font-variant-alternates,font-variant-ligatures, font-variant-east-asian, font-variant-numeric
normal|small-caps

  - @font-face
  


#### css dom

#### css jquery

## DOMタグ操作
document.querySelect(selector)->tag
- Image API
new Image()->img
img.src

- iframe
iframe_tag.windowcontent.document.xxx


#### event

- MouseEvent
onmouseup=(event)=>{}
onmousedown=(event)=>{}
onmousewheel=(event)=>{}

| method | valueType |
| ----- | ----- |
| event.altKey | bool |
| event.ctrlKey | bool |
| event.shiftKey | bool |
| event.metaKey | bool |
| clientX | integer |
| clientY | integer |
| screenX | integer |
| screenY | integer |


clientX, clientY: within the application's client area

- KeyboardEvent
onkeydown=(event)=>{}
onkeyup=(event)=>{}
onkeypress=(event)=>{}

| method | valueType |
| ----- | ----- |
| event.altKey | bool |
| event.ctrlKey | bool |
| event.shiftKey | bool |
| event.metaKey | bool |
| event.key | string(key name) |
| event.keyCode | Integer(key code) |
| event.repeat | bool(キー押し続くときはtrue表示する) |



##### key code

| key  | code  | key  | code  | key  | code  | key  | code  |
| ------------ | ------------ | ------------ | ------------ | ------------ | ------------ | ------------ | ------------ |
| \` | 192 | 1 | 49 | 2 | 50 | 3 | 51 |
| 4 | 52 | 5 | 53 | 6 | 54 | 7 | 55 |
| 8 | 56 | 9 | 57 | 0 | 48 | - | 189 |
| = | 187 | q | 81 | w | 87 | e | 69 |
| r | 82 | t | 84 | y | 89 | u | 85 |
| i | 73 | o | 79 | p | 80 | [ | 219 |
| ] | 221 | \ | 220 | a | 65 | s | 83 |
| d | 68 | f | 70 | g | 71 | h | 72 |
| j | 74 | k | 75 | l | 76 | ; | 186 |
| ' | 222 | z | 90 | x | 88 | c | 67 |
| v | 86 | b | 66 | n | 78 | m | 77 |
| , | 188 | . | 190 | / | 191 | [space] | 32 |
| [Tab] | 9 | [CapsLock] | 20 | [Shift] | 16 | [Control] | 17 |
| [Alt] | 18 | [Meta] | 91 | [Escape] | 27 | Backspace | 8 |
| F1 | 112 | F2 | 113 | F3 | 114 | F4 | 115 |
| F5 | 116 | F6 | 117 | F7 | 118 | F8 | 119 |
| F9 | 120 | F10 | 121 | F12 | 123 | [ArrowUp] | 38 |
| [ArrowDown] | 40 | [ArrowLeft] | 37 | [ArrowRight] | 39 | [enter] | 13 |



## canvas API

[参考](https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D "参考")
to get a `CanvasRenderingContext2D` instance, must first have a canvas element to work
```
const canvas = document.getElementById("cav");
const ctx = canvas.getContext("2d");
```
- draw
ctx.beginPath()  start a path
ctx.closePath() 　自動的に形を囲む
ctx.fill()
ctx.stroke()  描く

- save and restore
プロパティを保存と再生
ctx.restore()
ctx.save()

#### ライン
ctx.moveTo(x,y)　　定義
ctx.lineTo(x,y)　　定義
ctx.setLineDash(segment=[])
ctx.getLineDash()

- segment:
  [黒,白,黒,白] => [1,2,1,2]
ctx.lineWidth
ctx.lineJoin = bevel || round || miter
ctx.lineCap = butt || round || square

#### 四角い
ctx.strokeRect(x,y,w,h)
ctx.fillRect(x,y,w,h)
ctx.clearRect(x,y,w,h)

#### 丸
ctx.arc(x, y, radius, )
ctx.arcTo(x1,y1, x2,y2,radius)
bezier曲線:
ctx.bezierCurveTo(cp1.x,cp1.y,cp2.x,cp2.y,end.x,end.y)
ctx.quadraticCurveTo(cp.x,cp.y, end.x,end.y)

扇形を描く：
```
ctx.fillStyle = "blue"   # 青色の内容
ctx.strokeStyle = "blue"  #　青色のライン
ctx.beginPath();  # パスを開始
ctx.moveTo(100, 75);  # 丸の中心点
ctx.arc(100, 75, 50, 0, Math.PI/2);  # 四分の丸を描く
ctx.closePath();   # パスを終わり
ctx.fill()  # 内容を満たす準備
ctx.stroke()  # 描く
```

#### 文字
ctx.fillText(text, x, y)
ctx.strokeText(text, x, y)

ctx.font = "50px arial"
ctx.textAlign = left || right || center || start || end
ctx.textBaseLine
#### 画面を切る
ctx.clip()
ctx.clip(path)
```
var region = new Path2D();
region.arc(50,50,50,0,Math.PI*2)
ctx.clip(region)
```

#### style:
css color, gradient, pattern
- css color
blue, green, yellow ..., rgb(x,y,z),...
- gradient
linear gradient「線形」, radial gradient「円形」
  - linear gradient
	ctx.createLinearGradient(x1,x2,y1,y2) -> CanvasGradient
	gradient.addColorStop(offset, color)

	```
	const canvas = document.getElementById('cav');
    const ctx = canvas.getContext('2d');
    // Create circular clipping region
    var linear_gradient = ctx.createLinearGradient(20,0, 100,0);
    linear_gradient.addColorStop(0, "green");
    linear_gradient.addColorStop(1, "blue");

    ctx.beginPath();
    ctx.fillStyle = linear_gradient;

    ctx.arc(100,100,100,0,Math.PI*2);
    ctx.closePath();
    ctx.fill();
    ctx.stroke();
	```
  - radial gradient
	ctx.createRadialGradient(x1,x2,r1,y1,y2,r2) -> CanvasGradient

##### pattern:
ctx.createPattern(img_handle, repetition?"repeat") -> CanvasPattern
  - img
  HTMLImageElement, SVGImageElement, HTMLVideoElement, HTMLCanvasElement, ImageBitmap

##### image data
毎一つdataは四つのbitを占める、rgba
ctx.createImageData(dx,dy) -> ImageData

```
ctx.createImageData(100, 100) #100*100/4のData数正方形で揃う、毎一つDataは四つのByteを占める、dataはobj.dataに配列で保存している
// Iterate through every pixel
for (let i = 0; i < imageData.data.length; i += 8) {

// Modify pixel data
imageData.data[i + 0] = 255;  // R value
imageData.data[i + 1] = 0;    // G value
imageData.data[i + 2] = 0;  // B value
imageData.data[i + 3] = 255;  // A value
}

// Draw image data to the canvas
ctx.putImageData(imageData, 20, 20);
```
ctx.getImageData(x1,x2,y1,y2)
ctx.putImageData(image_data, x, y)
```
ctx.rect(10, 10, 100, 100);
ctx.fill();

let imageData = ctx.getImageData(60, 60, 200, 100); // copy image that existed
ctx.putImageData(imageData, 150, 10);
```
##### イメージ
ctx.drawImage(img)
ctx.drawImage(img, sx,sy,swidth,sheight, dx,dy,dw,dh) -> CanvasDrawImage
- img
  HTMLImageElement, SVGImageElement, HTMLVideoElement, HTMLCanvasElement, ImageBitmap

##### rotate
ctx.translate(x,y)  totateするときの原点matrix
ctx.rotate(angle)
ctx.setTransform(a,b,c,d,e,f) == ctx.transform(a,b,c,d,e,f)

##### 効果
ctx.shadowColor = "red"
ctx.shadowBlur = 15
ctx.shadowOffsetX, ctx.shadowOffsetY
ctx.imageSmoothEnabled = true

#### Path2D
Path2D()
CanvasPattern()
CanvasGradient()
...

## webgl
