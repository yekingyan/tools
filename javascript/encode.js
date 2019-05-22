export const utf8_to_b64 = (str) => {
  return window.btoa(unescape(encodeURIComponent(str)))
}

/**
* utf8_to_b64('✓ à la mode'); // JTI1dTI3MTMlMjUyMCUyNUUwJTI1MjBsYSUyNTIwbW9kZQ==
* b64_to_utf8('JTI1dTI3MTMlMjUyMCUyNUUwJTI1MjBsYSUyNTIwbW9kZQ=='); // "✓ à la mode"
* 
* utf8_to_b64('I \u2661 Unicode!'); // SSUyNTIwJTI1dTI2NjElMjUyMFVuaWNvZGUlMjUyMQ==
* b64_to_utf8('SSUyNTIwJTI1dTI2NjElMjUyMFVuaWNvZGUlMjUyMQ=='); // "I ♡ Unicode!"
*/

export const b64_to_utf8 = (str) => {
  return decodeURIComponent(escape(window.atob(str)))
}
