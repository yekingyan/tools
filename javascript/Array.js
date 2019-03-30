/**
 * 数组去重  ---------------------------------
 */

//Set1
function unique(arr) {
    return Array.from(new Set(arr))
}

//Set2
function unique2(arr) {
    return [...new Set(arr)]
}

// Map + filter()
function unique(arr) {
    const seen = new Map()
    return arr.filter((a) => !seen.has(a) && seen.set(a, 1))
}

// for...of + Object
function distinct(a, b) {
    let arr = a.concat(b)
    let result = []
    let obj = {}

    for (let i of arr) {
        if (!obj[i]) {
            result.push(i)
            obj[i] = 1
        }
    }

    return result
}


/**
 * 判断数组中是否存在某个值 ---------------------------------
 */

// array.includes()
let numbers = [12, 5, 8, 130, 44];
let numbers = [12, 5, 8, 130, 44];
let result = numbers.includes(8);
// 结果： true
result = numbers.includes(118)
// 结果： false


// array.indexOf()
let arr = ['something', 'anything', 'nothing', 'anything'];
let index = arr.indexOf('nothing');
// 结果：2


//array.find()
let numbers = [12, 5, 8, 130, 44];
let result = numbers.find(item => {
    return item > 8;
});
// 结果： 12

let items = [
    {id: 1, name: 'something'},
    {id: 2, name: 'anything'},
    {id: 3, name: 'nothing'},
    {id: 4, name: 'anything'}
];
let item = items.find(item => {
    return item.id === 3;
});
//  结果： Object { id: 3, name: "nothing" }


/**
 * 删除数组中一特定元素 ---------------------------------
 */
const removeElement = (array, element) => {
    
    let index = array.indexOf(element)
      if (index > 0) {
        return array.splice(index, 1)
      }
  }