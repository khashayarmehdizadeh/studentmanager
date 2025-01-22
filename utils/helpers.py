def validate_input(name,lastname,grade1,grade2):
    if not name or not lastname or not grade1 or not grade2:
        try:
            grade1=float(grade1)
            grade2=float(grade2)

            if not (0<=grade1 <=20 and 0<= grade2 <= 20):
                return False
            
        except ValueError:
            return False
        return True
        