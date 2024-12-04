use std::{cmp, env, fs::File, io, io::BufRead, path::Path};

fn read_input(path: &Path) -> io::Result<Vec<String>> {
    let file = File::open(path)?;
    let mut data: Vec<String> = Vec::new();
    for line in io::BufReader::new(file).lines() {
        data.push(line?);
    }
    Ok(data)
}

#[derive(Clone, Debug)]
struct GridScan {
    start: (usize, usize),
    end: (usize, usize),
    step: (isize, isize),
}

impl Iterator for GridScan {
    type Item = (usize, usize);

    fn next(&mut self) -> Option<Self::Item> {
        let curr = self.start;
        if curr == self.end {
            return None
        }
        let (mut x, mut y) = curr;
        let (dx, dy) = self.step;
        x = x.wrapping_add_signed(dx);
        y = y.wrapping_add_signed(dy);
        self.start = (x, y);
        Some(curr)
    }
}

impl DoubleEndedIterator for GridScan {
    fn next_back(&mut self) -> Option<Self::Item> {
        let curr = self.end;
        if curr == self.start {
            return None
        }
        let (mut x, mut y) = curr;
        let (dx, dy) = self.step;
        x = x.wrapping_add_signed(-dx);
        y = y.wrapping_add_signed(-dy);
        self.end = (x, y);
        Some(self.end)
    }
}

fn scan_horizontal(width: usize, height: usize) -> Box<dyn Iterator<Item=Box<GridScan>>> {
    Box::new((0..height).map(move |y|
        Box::new(GridScan { start: (0, y), end: (width, y), step: (1, 0) })
    ))
}

fn scan_vertical(width: usize, height: usize) -> Box<dyn Iterator<Item=Box<GridScan>>> {
    Box::new((0..width).map(move |x|
        Box::new(GridScan { start: (x, 0), end: (x, height), step: (0, 1) })
    ))
}

fn scan_diag_backslash(width: usize, height: usize) -> Box<dyn Iterator<Item=Box<GridScan>>> {
    Box::new(
        (0..width).map(move |x| {
            let num_steps = cmp::min(width - x, height);
            Box::new(GridScan { start: (x, 0), end: (x + num_steps, num_steps), step: (1, 1) })
        }).chain((1..height).map(move |y| {
            let num_steps = cmp::min(width, height - y);
            Box::new(GridScan { start: (0, y), end: (num_steps, y + num_steps), step: (1, 1) })
        }))
    )
}

fn scan_diag_slash(width: usize, height: usize) -> Box<dyn Iterator<Item=Box<GridScan>>> {
    Box::new(
        (0..width).map(move |x| {
            let num_steps = cmp::min(width - x, height);
            Box::new(GridScan { start: (x, height - 1), end: (x + num_steps, (height - 1).wrapping_sub(num_steps)), step: (1, -1) })
        }).chain((0..height - 1).map(move |y| {
            let num_steps = cmp::min(width, y + 1);
            Box::new(GridScan { start: (0, y), end: (num_steps, y.wrapping_sub(num_steps)), step: (1, -1) })
        }))
    )
}

fn bidirectional(scanners: Box<dyn Iterator<Item=Box<GridScan>>>) -> Vec<Box<dyn Iterator<Item=(usize, usize)>>> {
    let mut output: Vec<Box<dyn Iterator<Item=(usize, usize)>>> = Vec::new();
    for scanner in scanners {
        output.push(Box::new(scanner.clone()));
        output.push(Box::new(scanner.clone().rev()));
    }
    output
}

const SCANNERS: [fn(usize, usize) -> Box<dyn Iterator<Item=Box<GridScan>>>; 4] = [
    scan_horizontal,
    scan_vertical,
    scan_diag_backslash,
    scan_diag_slash,
];

fn scan_grid(width: usize, height: usize) -> impl Iterator<Item=Box<dyn Iterator<Item=(usize, usize)>>> {
    SCANNERS.iter().flat_map(move |scanner|
        bidirectional(scanner(width, height))
    )
}

fn solve(grid: &Vec<String>) {
    let height = grid.len();
    let width = grid[0].len();
    let count: usize = scan_grid(width, height).into_iter().map(|scanner| {
        let line: String = scanner.map(|(x, y)| grid[y].chars().nth(x).unwrap()).collect();
        line.matches("XMAS").count()
    }).sum();
    println!("{count}");
}

fn main() {
    for arg in env::args().skip(1) {
        println!("=== {arg}");
        let data = read_input(Path::new(&arg)).expect("reading input");
        solve(&data);
    }
}
