/*
Điều khiển hướng lái động cơ và tốc độ PWM bằng arduino khi đưa gia trị đã được sử lí
*/


const int ENA = 8;
const int IN1 = 9;
const int IN2 = 10;
const int ENB = 5;
const int IN3 = 6;
const int IN4 = 7;

void setup() {
  Serial.begin(9600);

  // Khởi tạo các chân 
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(ENA, OUTPUT);

  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  pinMode(ENB, OUTPUT);

  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);

  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');

    // Turn Right
    if (command[0] == 'R') 
    {
      int speed = command.substring(1).toInt();
      digitalWrite(IN1, LOW);
      digitalWrite(IN2, HIGH);
      analogWrite(ENA, speed);
    } 

    // Turn Left
    else if (command[0] == 'L') 
    {
      int speed = command.substring(1).toInt();
      digitalWrite(IN1, HIGH);
      digitalWrite(IN2, LOW);
      analogWrite(ENA, speed);
    } 

    // Forward
    else if (command[0] == 'F') {
      // Stop motor
      digitalWrite(IN1, LOW);
      digitalWrite(IN2, LOW);
      analogWrite(ENA, 0);
    }

    // Stop all motor
    else if (command[0] == 'S') {
      // Stop motor
      digitalWrite(IN1, LOW);
      digitalWrite(IN2, LOW);
      digitalWrite(IN3, LOW);
      digitalWrite(IN4, LOW);
      analogWrite(ENA, 0);
      analogWrite(ENB, 0);
    }

    // Run Motor 
    if (command[0] == 'C') 
    {
      int speed = command.substring(1).toInt();
      digitalWrite(IN3, LOW);
      digitalWrite(IN4, HIGH);
      analogWrite(ENB, speed);
    } 
  }
}
