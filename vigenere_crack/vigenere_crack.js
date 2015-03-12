Selectors = {
    encryptedText: '#encrypted',
    decryptedText: '#decrypted',
    encryptionKey: '#encryptionKey'
}

Settings = {
    debug: true
}

function init() {
    Listeners.addDecryptListener();
}

function d(obj) {
    if (Settings.debug)
        console.log(obj);
}

var Vigenere = {
    decrypt: function(encrypted, key) {
        // Source: http://www.nayuki.io/res/vigenere-cipher-javascript.js
        for (var i = 0; i < key.length; i++)
            key[i] = (26 + key[i]) % 26;
        
        return Vigenere.encrypt(encrypted, key);
    },    
    encrypt: function(input, key) {
        // Source: http://www.nayuki.io/res/vigenere-cipher-javascript.js
        var output = "";
        for (var i = 0, j = 0; i < input.length; i++) {
            var c = input.charCodeAt(i);
            var diff, shouldRewrite = true;
            if (isUppercase(c)) {
                diff = 65;
            } else if (isLowercase(c)) {
                diff = 97;
            } else {
                output += input.charAt(i);
                continue;
            }
                
            output += String.fromCharCode((c + key.charCodeAt(j%key.length) - diff - 65) % 26 + diff);
            j++;
        }
        
        return output;
    }    
}

var Listeners = {
    addDecryptListener: function() {
        $(Selectors.encryptedText).on("change keyup paste", function() {
            d(Selectors.encryptedText + ' change fired');
            exec();
        });
        
        $(Selectors.encryptionKey).on("change keyup paste", function() {
            d(Selectors.encryptionKey + ' change fired');            
            exec();
        });
        
        function exec() {
            var encrypted = $(Selectors.encryptedText).val();
            var key = $(Selectors.encryptionKey).val().toUpperCase();

            var decrypted = Vigenere.encrypt(encrypted, key);
            $(Selectors.decryptedText).val(decrypted);
        }
    }
}

/** Helper functions **/
// Tests whether the specified character code is a letter.
function isLetter(c) {
	return isUppercase(c) || isLowercase(c);
}

// Tests whether the specified character code is an uppercase letter.
function isUppercase(c) {
	return c >= 65 && c <= 90;  // 65 is the character code for 'A'. 90 is for 'Z'.
}

// Tests whether the specified character code is a lowercase letter.
function isLowercase(c) {
	return c >= 97 && c <= 122;  // 97 is the character code for 'a'. 122 is for 'z'.
}