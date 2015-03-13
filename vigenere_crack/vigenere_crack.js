Selectors = {
    encryptedText: '#encrypted',
    decryptedText: '#decrypted',
    encryptionKey: '#encryptionKey',
    modeSelector: '#modeSelector'
}

Settings = {
    debug: true,
    mode: {
        encypt: 'encrypt',
        decrypt: 'decrypt',
        actual: undefined
    }
}

function init() {
    Listeners.addDecryptListener();
    Listeners.addChangeModeListener();
}

function d(obj) {
    if (Settings.debug)
        console.log(obj);
}

var Vigenere = {
    decrypt: function(input, key) {
        key = Vigenere.preprocessKey(key, true);
        return Vigenere.calculate(input, key);
    },    
    
    encrypt: function(input, key) {
        key = Vigenere.preprocessKey(key, false);
        return Vigenere.calculate(input, key);
    },
    
    calculate: function(input, key) {
        var output = "";
        for (var i = 0, j = 0; i < input.length; i++) {
            var c = input.charCodeAt(i);
            var base = 0;
            
            if (isUppercase(c))
                base = 'A'.charCodeAt(0);
            else if (isLowercase(c))
                base = 'a'.charCodeAt(0);
            else {
                output += input.charAt(i);
                continue;
            }
            
            if (Settings.mode.actual === Settings.mode.decrypt && c === 65)
                console.log('test');
            
            
            var a = (c + key[j%key.length] - base);
            var b = a%26;
            var d = b + base;
            output += String.fromCharCode(d);
            j++;
        }
        
        return output;
    },
    
    preprocessKey: function(key, toDecrypt) {
        key = key.toUpperCase();
        var output = [];
        for(var i=0; i<key.length; ++i) {
            var val = key.charCodeAt(i) - 'A'.charCodeAt(0);
            
            if (toDecrypt === true)
                val *= -1;
            
            output.push(val);
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

            if (Settings.mode.actual === Settings.mode.encypt) {
                var result = Vigenere.encrypt(encrypted, key);
            } else {
                var result = Vigenere.decrypt(encrypted, key);
            }
            
            $(Selectors.decryptedText).val(result);
        }
    },
    
    addChangeModeListener: function() {
        Settings.mode.actual = Settings.mode.encypt;
        
        $(Selectors.modeSelector).on('click', function() {
            Settings.mode.actual = (Settings.mode.actual === Settings.mode.encypt) 
                ? Settings.mode.decrypt
                : Settings.mode.encypt;
            
            $(Selectors.modeSelector).val(Settings.mode.actual);
            $(Selectors.modeSelector).html('Mode: ' + Settings.mode.actual);
            $(Selectors.encryptedText).trigger('change');
        })
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