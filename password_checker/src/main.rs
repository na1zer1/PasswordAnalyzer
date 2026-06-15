use std::io::{self, Read}; // Импортируем отдельно блок io и отдельно трейт Read из блока io

fn main() {
    let mut password: String = String::new();
    let length: usize;
    let mut is_upper_case: bool = false;
    let mut is_num: bool = false;
    let mut is_spec_symbol: bool = false;

    match io::stdin().read_to_string(&mut password) {
        Ok(_) => {},
        Err(e) => eprint!("{e}")
    }

    let clean_password: &str = password.trim();

    // Длина
    length = clean_password.len();

    // Содержиться ли верхний регистр
    check_upper_case(&clean_password, &mut is_upper_case);

    // Проверка на наличие цифры
    check_num(&clean_password, &mut is_num);

    // Есть ли спец символы?
    check_symbols(&clean_password, &mut is_spec_symbol);
    
    print!("password:{clean_password}\nlength:{length}\nupper_cases_in:{is_upper_case}\ndigits_in:{is_num}\nspec_symbols_in:{is_spec_symbol}");
}

fn check_upper_case(password: &str, is_upper_case: &mut bool) {
    let mut res: bool = false;
    for i in password.chars() {
        if i.is_uppercase() {
            res = true;
        }
    }
    *is_upper_case = res; // * - Обращаемся по ссылке к переменной is_upper_case, лежащей в аргументе is_upper_case и меняем значение
}

fn check_num(password: &str, is_num: &mut bool) {
    let mut res: bool = false;
    for i in password.chars() {
        if i.is_digit(10) {
            res = true;
        }
    }
    *is_num = res;
}

fn check_symbols(password: &str, is_spec_symbol: &mut bool) {
    let mut res: bool = false;
    for i in password.chars() {
        if !i.is_alphanumeric() {
            res = true;
        }
    }
    *is_spec_symbol = res;
}
