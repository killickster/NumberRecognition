const request = require('request')
const http = require('http')

var canvas = document.getElementById("drawingCanvas")

var gl = canvas.getContext('webgl', {preserveDrawingBuffer:true})


var vertexBuffer = gl.createBuffer()


const vertCode = 'precision mediump float;' +
                'attribute vec2 coordinates;'+
                'attribute float vertColor;'+
                'varying vec4 fragColor;'+
                'void main(){' +
                'fragColor = vec4(vertColor, vertColor, vertColor, 1);'+
                'gl_Position = vec4(coordinates,0,1);'+
                '}'

const vertShader = gl.createShader(gl.VERTEX_SHADER);


gl.shaderSource(vertShader, vertCode)

gl.compileShader(vertShader)

if(!gl.getShaderParameter(vertShader, gl.COMPILE_STATUS)){
    console.log(gl.getShaderInfoLog(vertShader))
}

const fragCode = 'precision mediump float;' +
                'varying vec4 fragColor;' +
                'void main(){' +
                'gl_FragColor = vec4(fragColor);'+
                '}'

var fragShader = gl.createShader(gl.FRAGMENT_SHADER)

gl.shaderSource(fragShader, fragCode)

gl.compileShader(fragShader)

if(!gl.getShaderParameter(fragShader, gl.COMPILE_STATUS)){
    console.log(gl.getShaderInfoLog(fragShader))
}

const shaderProgram = gl.createProgram()

gl.attachShader(shaderProgram, fragShader)

gl.attachShader(shaderProgram, vertShader)

gl.linkProgram(shaderProgram)

gl.useProgram(shaderProgram)


function drawPixel(x,y,color){

    new Promise((resolve, reject) => {

        var sizeOfPixel = 2/28

        var renderX = pixelToRenderCoordinateX(x)
        var renderY = pixelToRenderCoordinateY(y)
        var renderColor = greyScalePixelFloatValue(color)

        var verticies = [
            renderX, renderY, renderColor,
            renderX + sizeOfPixel, renderY, renderColor,
            renderX + sizeOfPixel, renderY + sizeOfPixel, renderColor,
            renderX, renderY + sizeOfPixel, renderColor
        ]

        var indicies = [
            0,1,2,
            2,3,0
        ]

        pixelData = {verticies, indicies}

        resolve(pixelData)


    }).then((pixel) => {

        var vertexBuffer = gl.createBuffer()

        gl.bindBuffer(gl.ARRAY_BUFFER, vertexBuffer)

        gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(pixel.verticies), gl.STATIC_DRAW)

        var indexBuffer = gl.createBuffer()

        gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, indexBuffer)

        gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, new Uint16Array(pixel.indicies), gl.STATIC_DRAW)

        const coord = gl.getAttribLocation(shaderProgram, "coordinates")
        const color = gl.getAttribLocation(shaderProgram, "vertColor")

        gl.vertexAttribPointer(coord,
            2,
            gl.FLOAT,
            false,
            3*Float32Array.BYTES_PER_ELEMENT,
            0
            )

        gl.vertexAttribPointer(color,
            1,
            gl.FLOAT,
            false,
            3*Float32Array.BYTES_PER_ELEMENT,
            2*Float32Array.BYTES_PER_ELEMENT
            )

        gl.enableVertexAttribArray(color)
        gl.enableVertexAttribArray(coord)


        gl.disable(gl.DEPTH_TEST);

        gl.viewport(0,0,gl.drawingBufferWidth, gl.drawingBufferHeight);

        gl.drawElements(gl.TRIANGLES, pixel.indicies.length,gl.UNSIGNED_SHORT,0)
    })

}

function clearCanvas(){
    clearPixels()

    gl.clearColor(1,1,1,1)

    gl.clear(gl.COLOR_BUFFER_BIT)
}

function pixelToCanvasPointX(pixel){
    return pixel/27*canvas.width;
}

function pixelToCanvasPointY(position){
    return pixel/27*canvas.height;
}

function canvasPointToPixelX(pointX){
    return Math.floor(pointX/canvas.width * 27)
}

function canvasPointToPixelY(pointY){
    return Math.floor(pointY/canvas.height * 27)
}


this.canvas.addEventListener("mousedown", e => {
    this.dragging = true 
    this.lastX = e.x;
    this.lastY = e.y;

 })

 this.canvas.addEventListener("mouseup", e => {
     this.dragging = false;
 })

var pixelDictionary = {}

 this.canvas.addEventListener("mousemove", e => {
     if(this.dragging){
         console.log(pixelDictionary)
        
        x = canvasPointToPixelX(e.x)
        y = canvasPointToPixelY(e.y)



        x1 = canvasPointToPixelX(e.x)
        y1 = canvasPointToPixelY(e.y + 1/27*canvas.height)
        x2 = canvasPointToPixelX(e.x)
        y2 = canvasPointToPixelY(e.y - 1/27*canvas.height)
        x3 = canvasPointToPixelX(e.x+1/27*canvas.width)
        y3 = canvasPointToPixelY(e.y)
        x4 = canvasPointToPixelX(e.x-1/27*canvas.width)
        y4 = canvasPointToPixelY(e.y)



        pixelIntensity(pixelToIndex(x,y), 255/255)
        drawPixel(x,y,255)

        if(!pixelDictionary[(x1,y1)]){
            drawPixel(x1,y1, 200)
            pixelIntensity(pixelToIndex(x1,y1),200/255)
        }
        
        if(!pixelDictionary[(x2,y2)]){
            drawPixel(x2,y2, 200)
            pixelIntensity(pixelToIndex(x2,y2),200/255)
        }

        if(!pixelDictionary[(x3,y3)]){
            drawPixel(x3,y3, 200)
            pixelIntensity(pixelToIndex(x3,y3),200/255)
        }

        if(!pixelDictionary[(x4,y4)]){
            drawPixel(x4,y4, 200)
            pixelIntensity(pixelToIndex(x4,y4),200/255)
        }

        pixelDictionary[(x,y)] = true


        console.log("x: " + x)
        console.log("y: " +y)

     }
 })


 function pixelToIndex(x,y){


     console.log(y*28 + x)
     return y*28 + x


 }






/*
This function takes a pixel x where x can range 0-2
and converts it to the rendering
coordinate system which goes from -1 to 1 
*/
function pixelToRenderCoordinateX(x){
    return (2*x)/26-1
}

/*
This function takes a pixel y where y canrange 0-27
and converts it to the rendering
coordinate system which goes from -1 to 1 
*/

function pixelToRenderCoordinateY(y){
    return -((2*y)/27-1)
}

function renderCoordinateToPixelX(x){
    return Math.floor((x+1)*27/2)
}

function renderCoordinateToPixelY(y){
    return Math.floor((y+1)*27/2)
}

function greyScalePixelFloatValue(c){
    return 1-c/256
}

function floatToGreyScale(c){
    return Math.floor((c-1)*256)
}

function clearPixels(){

    request.delete("http://localhost:5000/clear")

}
function decodeNumber(){
    console.log("decode")
    request.get('http://localhost:5000/decode').on('response', function(response){
        console.log(response.statusMessage)
    })

    pixelDictionary = {}


}


function pixelIntensity(pixel, intensity){

    console.log("calling")

    const data = JSON.stringify({
        'data': intensity
    })


    var path = "/pixel/" + pixel

    const options = {
        hostname: 'localhost',
        port: 5000,
        path: path,
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'Content-Length' : data.length
        }
        
    }


    const req = http.request(options, res => {
        console.log(`status code: ${res.statusCode}`)


        res.on('data', d => {
            process.stdout.write(d)
        })
    })


    req.on('error', error => {
        console.error(error)
      })
      
      req.write(data)
      req.end()


}





function showPixels(){
    request.get('http://localhost:5000/show').on('response', function(response){
        console.log(response.statusCode)
    })
}




