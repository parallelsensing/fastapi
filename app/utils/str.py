def process_number(num):
  tens_digit = (num // 10) % 10
  units_digit = num % 10
  return f"{tens_digit}{units_digit}"