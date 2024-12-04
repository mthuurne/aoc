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

impl GridScan {
    fn horizontal(width: usize, height: usize) -> impl Iterator<Item=GridScan> {
        (0..height).map(move |y|
            GridScan { start: (0, y), end: (width, y), step: (1, 0) }
        )
    }

    fn vertical(width: usize, height: usize) -> impl Iterator<Item=GridScan> {
        (0..width).map(move |x|
            GridScan { start: (x, 0), end: (x, height), step: (0, 1) }
        )
    }

    fn backslash(width: usize, height: usize) -> impl Iterator<Item=GridScan> {
        (0..width).map(move |x| {
            let num_steps = cmp::min(width - x, height);
            GridScan { start: (x, 0), end: (x + num_steps, num_steps), step: (1, 1) }
        }).chain((1..height).map(move |y| {
            let num_steps = cmp::min(width, height - y);
            GridScan { start: (0, y), end: (num_steps, y + num_steps), step: (1, 1) }
        }))
    }

    fn slash(width: usize, height: usize) -> impl Iterator<Item=GridScan> {
        (0..width).map(move |x| {
            let num_steps = cmp::min(width - x, height);
            GridScan { start: (x, height - 1), end: (x + num_steps, (height - 1).wrapping_sub(num_steps)), step: (1, -1) }
        }).chain((0..height - 1).map(move |y| {
            let num_steps = cmp::min(width, y + 1);
            GridScan { start: (0, y), end: (num_steps, y.wrapping_sub(num_steps)), step: (1, -1) }
        }))
    }
}

fn bidirectional(scanners: impl Iterator<Item=GridScan>) -> impl Iterator<Item=Box<dyn Iterator<Item=(usize, usize)>>> {
    scanners.flat_map(|scanner| {
        let dirs: [Box<dyn Iterator<Item=(usize, usize)>>; 2] = [
            Box::new(scanner.clone()),
            Box::new(scanner.rev()),
        ];
        dirs.into_iter()
    })
}

const SCANNERS: [fn(usize, usize) -> Box<dyn Iterator<Item=GridScan>>; 4] = [
    |w, h| Box::new(GridScan::horizontal(w, h)),
    |w, h| Box::new(GridScan::vertical(w, h)),
    |w, h| Box::new(GridScan::backslash(w, h)),
    |w, h| Box::new(GridScan::slash(w, h)),
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
