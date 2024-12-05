use std::{collections::HashMap, env, fs::File, io::{self, BufRead}, path::Path};

fn read_input(path: &Path) -> io::Result<(Box<[(u64, u64)]>, Box<[Box<[u64]>]>)> {
    let file = File::open(path)?;
    let mut lines = io::BufReader::new(file).lines();

    let mut rules: Vec<(u64, u64)> = Vec::new();
    while let Some(line) = lines.next() {
        let text = line?;
        if text.is_empty() {
            break;
        }
        let values = text.split('|').map(
            |s| s.parse().expect("values must be integers")
        ).collect::<Vec<_>>();
        if values.len() != 2 {
            panic!("ordering must have two values");
        }
        rules.push((values[0], values[1]));
    }

    let mut books: Vec<Box<[u64]>> = Vec::new();
    for line in lines {
        let text = line?;
        let values = text.split(',').map(
            |s| s.parse().expect("values must be integers")
        ).collect::<Vec<_>>();
        books.push(values.into_boxed_slice());
    }

    Ok((rules.into_boxed_slice(), books.into_boxed_slice()))
}

fn solve(rules: &[(u64, u64)], books: &[Box<[u64]>]) {
    let mut score1 = 0;
    let mut score2 = 0;
    for book in books {
        // Use the fact that the input compares every page combination.
        let mut freqs: HashMap<u64, usize> = HashMap::with_capacity(book.len());
        for page in book {
            freqs.insert(*page, 0);
        }
        for (page1, page2) in rules {
            if freqs.contains_key(page1) {
                if let Some(count) = freqs.get_mut(page2) {
                    *count += 1;
                }
            }
        }
        let mut correct = Vec::from(&**book);
        correct.sort_by_key(|page| freqs.get(page).unwrap());

        println!("old: {book:?}");
        println!("new: {correct:?}");
        let middle = correct[book.len() / 2];
        if **book == correct {
            println!("right order, middle page is {middle}");
            score1 += middle;
        } else {
            println!("wrong order, middle page should be {middle}");
            score2 += middle;
        }
        println!();
    }
    println!("part 1 checksum: {score1}");
    println!("part 2 checksum: {score2}");
}

fn main() {
    for arg in env::args().skip(1) {
        println!("=== {arg}");
        let (rules, books) = read_input(Path::new(&arg)).expect("reading input");
        solve(&rules, &books);
    }
}
