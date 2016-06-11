#include <Wire.h>  
#include <LiquidCrystal_I2C.h>
LiquidCrystal_I2C lcd(0x27, 2, 1, 0, 4, 5, 6, 7, 3, POSITIVE);

void setup()
{
  Serial.begin(9600);

  lcd.begin(20, 4);
  lcd.backlight();
  lcd.setCursor(0, 0);
}

void loop()
{
  if (Serial.available()) {
    
    delay(100);  

    lcd.clear();
    int rowCounter = 0;
    int charactersRead = 0;
    while (Serial.available() > 0) {
      

      if (charactersRead && charactersRead % 20 == 0)
      {
        rowCounter = (rowCounter + 1) % 4; 
        lcd.setCursor(0, rowCounter);
      }
      
      charactersRead ++;
      
      lcd.write(Serial.read());
    }
  }
}

